"""TileRenderer class module."""

from PIL import ImageDraw

from heightmap_renderer._tile import _Tile
from heightmap_renderer.utils import (
    _CORNER_OFFSETS,
    DEBUG_OUTLINE_SHADE,
    DEBUG_OUTLINE_WIDTH,
    isometric_projection,
)


class _TileRenderer:
    """Renders a single tile."""

    def __init__(
        self,
        tile: None | _Tile,
        draw_context: ImageDraw.ImageDraw,
        scale: int,
        relief_scale: float,
        x_offset: int,
        y_offset: int,
        shader: str = "height",
        *,
        debug_renderer: bool,
    ) -> None:
        self.tile = tile
        self.draw_context = draw_context
        self.scale = scale
        self.relief_scale = relief_scale
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.color = 0
        self.shader = shader
        self.debug_renderer = debug_renderer

    def render(self) -> None:
        """Render the tile."""
        if not self.tile:
            raise TypeError  # type guard for mypy

        outline = DEBUG_OUTLINE_SHADE if self.debug_renderer else None
        width = DEBUG_OUTLINE_WIDTH if self.debug_renderer else 0

        draw_points = [
            isometric_projection(
                x=(self.tile.x + dx) * self.scale,
                y=(self.tile.y + dy) * self.scale,
                z=round(
                    self.tile.vertex_heights[count] * self.scale * self.relief_scale
                ),
                output_x_offset=self.x_offset,
                output_y_offset=self.y_offset,
            )
            for count, (dx, dy) in enumerate(_CORNER_OFFSETS)
        ]

        self.draw_context.polygon(
            xy=draw_points,
            fill=self.color,
            outline=outline,
            width=width,
        )
