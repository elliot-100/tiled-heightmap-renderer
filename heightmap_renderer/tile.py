"""Tile class module."""


class Tile:
    """Represents an abstract tile."""

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
            Height values.
        """
        self.x = x
        self.y = y
        self.heights = heights
