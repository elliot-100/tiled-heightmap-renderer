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

    @property
    def in_shadow(self) -> bool:
        input_offsets = [(-1, 1), (-1, 0), (0, 1)]
        x, y = self.location.x, self.location.y
        input_heights = [self.heightmap[x + dx][y + dy] for dx, dy in input_offsets]
        return any(h > self.heightmap[x][y] for h in input_heights)

    @property
    def tri1(self) -> dict[tuple[int, int], int]:
        return {
            (0, 0): self.vertex_heights[0],
            (0, 1): self.vertex_heights[1],
            (1, 1): self.vertex_heights[2],
        }

    @property
    def tri2(self) -> dict[tuple[int, int], int]:
        return {
            (0, 0): self.vertex_heights[0],
            (1, 0): self.vertex_heights[3],
            (1, 1): self.vertex_heights[2],
        }
