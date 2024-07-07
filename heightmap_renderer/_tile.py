"""Tile class module."""

from heightmap_renderer import _CORNER_OFFSETS


class _Tile:
    """Represents a quad tile on the heightmap."""

    def __init__(
        self,
        heightmap: list[list[int]],
        x: int,
        y: int,
    ) -> None:
        """
        Parameters
        ----------
        heightmap
        x
            Logical location on the heightmap.
        y
            Logical location on the heightmap.
        """
        self.x = x
        self.y = y
        self.heightmap = heightmap

    @property
    def vertex_heights(self) -> list[int]:
        return [
            self.heightmap[self.x + dx][self.y + dy] for (dx, dy) in _CORNER_OFFSETS
        ]
