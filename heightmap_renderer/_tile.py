"""Tile class module."""

from heightmap_renderer import _CORNER_OFFSETS
from heightmap_renderer._coordinate_int_2d import _CoordinateInt2D


class _Tile:
    """Represents a quad tile on the heightmap."""

    def __init__(self, heightmap: list[list[int]], location: _CoordinateInt2D) -> None:
        """
        Parameters
        ----------
        heightmap
        location
            Logical location on the heightmap.
        """
        self.location = location
        self.heightmap = heightmap

    @property
    def vertex_heights(self) -> list[int]:
        return [
            self.heightmap[(self.location + offset).x][(self.location + offset).y]
            for offset in _CORNER_OFFSETS
        ]
