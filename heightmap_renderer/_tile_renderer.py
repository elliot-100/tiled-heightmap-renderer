"""TileRenderer class module."""

import math
from typing import TYPE_CHECKING

from PIL import ImageDraw

from heightmap_renderer._coordinate_int_2d import _CoordinateInt2D
from heightmap_renderer.utils import (
    _CORNER_OFFSETS,
    DEBUG_OUTLINE_SHADE,
    DEBUG_OUTLINE_WIDTH,
    heightmap_highest,
    heightmap_lowest,
    heightmap_size,
    isometric_projection,
    normalise_8bit,
)

if TYPE_CHECKING:
    from heightmap_renderer._tile import _Tile


class _TileRenderer:
    """Renders a single tile."""

    def __init__(
        self,
        draw_context: ImageDraw.ImageDraw,
        scale: int,
        relief_scale: float,
        offset: _CoordinateInt2D,
        shader: str = "height",
        *,
        debug_renderer: bool,
    ) -> None:
        self.draw_context = draw_context
        self.scale = scale
        self.relief_scale = relief_scale
        self.offset = offset
        self.color = 0
        self.shader = shader
        self.debug_renderer = debug_renderer

        self.tile: _Tile | None = None

    def render(self) -> None:
        """Render the tile."""
        if not self.tile:
            raise TypeError  # type guard for mypy

        outline = DEBUG_OUTLINE_SHADE if self.debug_renderer else None
        width = DEBUG_OUTLINE_WIDTH if self.debug_renderer else 0

        draw_points = [
            isometric_projection(
                x=(self.tile.location.x + dx) * self.scale,
                y=(self.tile.location.y + dy) * self.scale,
                z=round(
                    self.tile.vertex_heights[count] * self.scale * self.relief_scale
                ),
                output_offset=self.offset,
            )
            for count, (dx, dy) in enumerate(_CORNER_OFFSETS)
        ]

        self.draw_context.polygon(
            xy=draw_points,
            fill=self._shade(),
            outline=outline,
            width=width,
        )

    def _shade(self) -> int:
        """Determine the tile colour (shade in current implementation)."""
        if not self.tile:
            raise TypeError  # type guard for mypy

        if self.shader == "depth":
            the_heightmap_size = heightmap_size(self.tile.heightmap)
            max_depth = math.sqrt(the_heightmap_size.x**2 + the_heightmap_size.y**2)
            depth = math.sqrt(self.tile.location.x**2 + self.tile.location.y**2)
            return normalise_8bit(depth, 0, max_depth)

        mean_height = sum(self.tile.vertex_heights) / 4
        return normalise_8bit(
            mean_height,
            heightmap_lowest(self.tile.heightmap),
            heightmap_highest(self.tile.heightmap),
        )
