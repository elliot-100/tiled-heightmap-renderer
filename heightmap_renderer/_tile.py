"""Tile class module."""

from heightmap_renderer._coordinate_int_2d import _CoordinateInt2D
from heightmap_renderer.utils import _CORNER_OFFSETS


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
            self.heightmap[self.location.x + dx][self.location.y + dy]
            for (dx, dy) in _CORNER_OFFSETS
        ]
