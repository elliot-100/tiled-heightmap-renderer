from __future__ import annotations

from typing import NamedTuple


class _CoordinateInt2D(NamedTuple):
    """Represents integer 2D coordinate."""

    x: int
    y: int

    def __add__(self, other: object) -> _CoordinateInt2D:
        if not isinstance(other, _CoordinateInt2D):
            err_msg = "Operand must be type `_CoordinateInt2D`."
            raise TypeError(err_msg)
        return _CoordinateInt2D(self.x + other.x, self.y + other.y)

    def __mul__(self, other: object) -> _CoordinateInt2D:
        if not isinstance(other, int):
            err_msg = "Operand must be type `int`."
            raise TypeError(err_msg)
        return _CoordinateInt2D(self.x * other, self.y * other)


ZERO_COORDINATE_2D = _CoordinateInt2D(0, 0)
