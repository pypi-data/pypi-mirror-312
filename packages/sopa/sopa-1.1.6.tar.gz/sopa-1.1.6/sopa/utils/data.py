from __future__ import annotations

import logging

import dask
import dask.array as da
import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter
from shapely.geometry import Point, box
from spatialdata import SpatialData
from spatialdata.datasets import BlobsDataset
from spatialdata.models import Image2DModel, PointsModel, ShapesModel
from spatialdata.transformations import Affine, Identity

from .._constants import SopaKeys
from ..patches.patches import _map_transcript_to_cell

dask.config.set({"dataframe.query-planning": False})
import dask.dataframe as dd  # noqa

log = logging.getLogger(__name__)


def uniform(
    *_,
    length: int = 2_048,
    cell_density: float = 1e-4,
    n_points_per_cell: int = 100,
    c_coords: list[str] = ["DAPI", "CK", "CD3", "CD20"],
    genes: int | list[str] = ["EPCAM", "CD3E", "CD20", "CXCL4", "CXCL10"],
    sigma_factor: float = 0.05,
    pixel_size: float = 0.1,
    seed: int = 0,
    include_vertices: bool = False,
    include_image: bool = True,
    apply_blur: bool = True,
    as_output: bool = False,
    transcript_cell_id_as_merscope: bool = False,
) -> SpatialData:
    """Generate a dummy dataset composed of cells generated uniformly in a square. It also has transcripts.

    Args:
        length: Size of the square, in pixels
        cell_density: Density of cells per pixel^2
        n_points_per_cell: Mean number of transcripts per cell
        c_coords: Channel names
        genes: Number of different genes, or list of gene names
        sigma_factor: Factor used to determine `sigma` for the gaussian blur.
        pixel_size: Number of microns in one pixel.
        seed: Numpy random seed
        include_vertices: Whether to include the vertices of the cells (as points) in the spatialdata object
        include_image: Whether to include the image in the spatialdata object
        apply_blur: Whether to apply gaussian blur on the image (without blur, cells are just one pixel)
        as_output: If `True`, the data will have the same format than an output of Sopa

    Returns:
        A SpatialData object with a 2D image (`sdata["image"]`), the cells polygon boundaries (`sdata["cells"]`), the transcripts (`sdata["transcripts"]`), and optional cell vertices (`sdata["vertices"]`) if `include_vertices` is `True`.
    """
    np.random.seed(seed)

    grid_width = max(1, int(length * np.sqrt(cell_density)))
    dx = length / grid_width
    sigma = dx * sigma_factor
    n_cells = grid_width**2
    radius = int(dx) // 4
    cell_types_index = np.random.randint(0, max(1, len(c_coords) - 1), n_cells)

    log.info(
        f"Image of size ({len(c_coords), length, length}) with {n_cells} cells and {n_points_per_cell} transcripts per cell"
    )

    ### Compute cell vertices (xy array)
    vertices_x = dx / 2 + np.arange(grid_width) * dx
    x, y = np.meshgrid(vertices_x, vertices_x)
    xy = np.stack([x.ravel(), y.ravel()], axis=1)
    xy += np.random.uniform(-dx / 2, dx / 2, size=xy.shape)
    xy = xy.clip(0, length - 1).astype(int)

    vertices = pd.DataFrame(xy, columns=["x", "y"])

    ### Create image
    images = {}

    if include_image:
        x_circle, y_circle = circle_coords(radius)

        image = np.zeros((len(c_coords), length, length))
        for i, (x, y) in enumerate(xy):
            y_coords = (y + y_circle).clip(0, image.shape[1] - 1)
            x_coords = (x + x_circle).clip(0, image.shape[2] - 1)
            image[0, y_coords, x_coords] = 1
            if len(c_coords) > 1:
                image[cell_types_index[i] + 1, y_coords, x_coords] = 1
        if apply_blur:
            image = gaussian_filter(image, sigma=sigma, axes=(1, 2))
        image = (image / image.max() * 255).astype(np.uint8)
        image = da.from_array(image, chunks=(1, 1024, 1024))
        images["image"] = Image2DModel.parse(image, c_coords=c_coords, dims=["c", "y", "x"])

    ### Create cell boundaries
    cells = [Point(vertex).buffer(radius).simplify(tolerance=1) for vertex in xy]
    bbox = box(0, 0, length - 1, length - 1)
    cells = [cell.intersection(bbox) for cell in cells]
    gdf = gpd.GeoDataFrame(geometry=cells)
    shapes = {"cellpose_boundaries" if as_output else "cells": ShapesModel.parse(gdf)}

    ### Create transcripts
    n_genes = n_cells * n_points_per_cell
    point_cell_index = np.arange(n_cells).repeat(n_points_per_cell)
    points_coords = radius / 2 * np.random.randn(n_genes, 2) + xy[point_cell_index]
    points_coords = points_coords.clip(0, length - 1)

    if isinstance(genes, int):
        gene_names = np.random.choice([chr(97 + i) for i in range(n_genes)], size=n_genes)
    elif len(genes) and len(genes) >= len(c_coords) - 1:
        gene_names = np.full(n_genes, "", dtype="<U5")
        for i in range(len(genes)):
            where_cell_type = np.where(cell_types_index[point_cell_index] == i)[0]
            probabilities = np.full(len(genes), 0.2 / (len(genes) - 1))
            probabilities[i] = 0.8
            gene_names[where_cell_type] = np.random.choice(genes, len(where_cell_type), p=probabilities)
    else:
        gene_names = np.random.choice(genes, size=n_genes)

    gene_names = gene_names.astype(object)
    gene_names[3] = np.nan  # Add a nan value for tests

    df = pd.DataFrame(
        {
            "x": points_coords[:, 0],
            "y": points_coords[:, 1],
            "z": 1,
            "genes": gene_names,
        }
    )

    # apply an arbritrary transformation for a more complete test case
    affine = np.array([[pixel_size, 0, 100], [0, pixel_size, 600], [0, 0, 1]])
    df[["x", "y", "z"]] = df[["x", "y", "z"]] @ affine.T
    affine = Affine(affine, input_axes=["x", "y"], output_axes=["x", "y"]).inverse()

    df = dd.from_pandas(df, chunksize=2_000_000)

    points = {"transcripts": PointsModel.parse(df, transformations={"global": affine, "microns": Identity()})}
    if include_vertices:
        points["vertices"] = PointsModel.parse(vertices)

    sdata = SpatialData(images=images, points=points, shapes=shapes)

    _map_transcript_to_cell(sdata, "cell_id", sdata["transcripts"], sdata["cells"])
    sdata["transcripts"]["cell_id"] = sdata["transcripts"]["cell_id"].astype(int) - int(transcript_cell_id_as_merscope)

    if as_output:
        _add_table(sdata)

    return sdata


def _add_table(sdata: SpatialData):
    from ..segmentation import Aggregator

    aggregator = Aggregator(sdata, shapes_key=SopaKeys.CELLPOSE_BOUNDARIES)

    aggregator.compute_table(gene_column="genes")


def circle_coords(radius: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute the coordinates of a circle

    Args:
        radius: Radius of the circle

    Returns:
        The x, y coordinates (two 1D ndarrays)
    """
    diameter = 2 * radius + 1
    mask = np.zeros((diameter, diameter), dtype=np.uint8)

    y, x = np.ogrid[: mask.shape[0], : mask.shape[1]]
    mask[((x - radius) ** 2 + (y - radius) ** 2) <= radius**2] = 1

    x_circle, y_circle = np.where(mask)
    return x_circle - radius, y_circle - radius


def blobs(
    *_,
    length: int = 1_024,
    n_points: int = 10_000,
    c_coords=["DAPI", "CK", "CD3", "CD20"],
    **kwargs,
) -> SpatialData:
    """Adapts the blobs dataset from SpatialData for sopa. Please refer to the SpatialData documentation"""
    _blobs = BlobsDataset(length=length, n_points=n_points, c_coords=c_coords, n_channels=len(c_coords), **kwargs)

    image = _blobs._image_blobs(
        _blobs.transformations,
        _blobs.length,
        _blobs.n_channels,
        _blobs.c_coords,
    )
    image.data = (image.data * 255).astype(np.uint8)

    points = _blobs._points_blobs(_blobs.transformations, _blobs.length, _blobs.n_points)
    genes = pd.Series(np.random.choice(list("abcdef"), size=len(points))).astype("category")
    points["genes"] = dd.from_pandas(genes, npartitions=points.npartitions)

    return SpatialData(images={"blob_image": image}, points={"blob_transcripts": points})
