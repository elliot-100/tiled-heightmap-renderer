"""Utility functions."""

import math

SQRT_2 = math.sqrt(2)

_CORNER_OFFSETS = [(0, 0), (0, 1), (1, 1), (1, 0)]

DEBUG_OUTLINE_SHADE = 255
DEBUG_OUTLINE_WIDTH = 1


def heightmap_size(heightmap: list[list[int]]) -> tuple[int, int]:
    """Get the size of the heightmap."""
    return len(heightmap), len(heightmap[0])


def heightmap_lowest(heightmap: list[list[int]]) -> int:
    """Find the lowest value in a heightmap."""
    lowest = min(min(row) for row in heightmap)
    if lowest < 0:
        err_msg = "Heightmap values must be >= 0."
        raise ValueError(err_msg)
    return lowest


def heightmap_highest(heightmap: list[list[int]]) -> int:
    """Find the highest value in a heightmap."""
    return max(max(row) for row in heightmap)


def normalise_8bit(value: float, lower_bound: float, upper_bound: float) -> int:
    """Normalise value to the range 0 <= n <= 255."""
    return int(255 * (value - lower_bound) / upper_bound - lower_bound)


def isometric_projection(
    x: int,
    y: int,
    z: int = 0,
    output_x_offset: int = 0,  # not sure if this belongs here
    output_y_offset: int = 0,
) -> tuple[float, float]:
    """Project heightmap coordinate to window (x, y) pixel coordinate.

    [Uses 'video game isometric' projection, i.e. dimetric projection with a 2:1
    pixel ratio]

    Parameters
    ----------
    x: int
    y: int
    z: int, optional
    output_x_offset: int, optional
    output_y_offset: int, optional

    Returns
    -------
    tuple[float, float]
    """
    output_x = (x - y) / SQRT_2 + output_x_offset
    output_y = (x + y) / SQRT_2 / 2 - z + output_y_offset
    return output_x, output_y
