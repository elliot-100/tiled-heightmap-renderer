from typing import NamedTuple


class _CoordinateInt2D(NamedTuple):
    """Represents integer 2D coordinate."""

    x: int
    y: int


ZERO_COORDINATE_2D = _CoordinateInt2D(0, 0)
