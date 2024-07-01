"""TileRenderer class module."""

from PIL import ImageDraw

from heightmap_renderer.tile import Tile
from heightmap_renderer.utils import CORNER_OFFSETS, isometric_projection


class TileRenderer:
    """Renders a single tile."""

    def __init__(
        self,
        tile: Tile,
        draw_context: ImageDraw.ImageDraw,
        scale: int,
        relief_scale: float,
        x_offset: int,
        y_offset: int,
        color: int,
    ) -> None:
        """
        Parameters
        ----------
        tile: Tile
            Tile to render.
        draw_context: ImageDraw.ImageDraw
        scale: int
        relief_scale: int
        x_offset: int
            Pixel offset.
        y_offset: int
            Pixel offset.
        color: int
        """
        self.tile = tile
        self.draw_context = draw_context
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.color = color
        self.points = [
            isometric_projection(
                x=(self.tile.x + dx) * scale,
                y=(self.tile.y + dy) * scale,
                z=round(self.tile.heights[count] * scale * relief_scale),
                output_x_offset=self.x_offset,
                output_y_offset=self.y_offset,
            )
            for count, (dx, dy) in enumerate(CORNER_OFFSETS)
        ]

    def render(self) -> None:
        """Render the tile."""
        self.draw_context.polygon(
            xy=self.points,
            fill=self.color,
            width=10,
        )
