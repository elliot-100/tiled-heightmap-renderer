"""Utility functions."""

from heightmap_renderer import _SQRT_2


def heightmap_size(heightmap: list[list[int]]) -> tuple[int, int]:
    """Return the size of the heightmap."""
    return len(heightmap), len(heightmap[0])


def heightmap_lowest(heightmap: list[list[int]]) -> int:
    """Return the lowest value in the heightmap."""
    lowest = min(min(row) for row in heightmap)
    if lowest < 0:
        err_msg = "Heightmap values must be >= 0."
        raise ValueError(err_msg)
    return lowest


def heightmap_highest(heightmap: list[list[int]]) -> int:
    """Return the highest value in the heightmap."""
    return max(max(row) for row in heightmap)


def normalise_8bit(
    value: float,
    values_lower_bound: float,
    values_upper_bound: float,
) -> int:
    """Return value normalised to the range `0 <= n <= 255`."""
    return int(
        255 * (value - values_lower_bound) / values_upper_bound - values_lower_bound
    )


def isometric_projection(
    x: int,
    y: int,
    z: int = 0,
    output_x_offset: int = 0,  # not sure if this belongs here
    output_y_offset: int = 0,
) -> tuple[float, float]:
    """Project `(x, y, z)` coordinate to `(x, y)` coordinate.

    NB: Uses 'video game isometric' projection, i.e. dimetric projection with a 2:1
    pixel ratio.

    Parameters
    ----------
    x
    y
    z : optional
    output_x_offset : optional
    output_y_offset : optional

    Returns
    -------
    tuple[float, float]
    """
    output_x = (x - y) / _SQRT_2 + output_x_offset
    output_y = (x + y) / _SQRT_2 / 2 - z + output_y_offset
    return output_x, output_y
