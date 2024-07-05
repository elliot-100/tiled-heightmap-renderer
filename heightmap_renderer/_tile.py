"""Tile class module."""


class _Tile:
    """Represents an abstract quad tile."""

    def __init__(
        self,
        x: int,
        y: int,
        heights: list[int],
    ) -> None:
        """
        Parameters
        ----------
        x: int
            Logical location on the heightmap.
        y: int
            Logical location on the heightmap.
        heights: list[int]
            Height values at the vertices.
        """
        self.x = x
        self.y = y
        self.heights = heights
