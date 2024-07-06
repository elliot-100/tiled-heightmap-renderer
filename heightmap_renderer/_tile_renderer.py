"""TileRenderer class module."""

import math
from typing import TYPE_CHECKING

from PIL import ImageDraw

from heightmap_renderer import (
    _CORNER_OFFSETS,
    _DEBUG_OUTLINE_SHADE,
    _DEBUG_OUTLINE_WIDTH,
)
from heightmap_renderer._tile import _Tile
from heightmap_renderer.utils import (
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
        x_offset: int,
        y_offset: int,
        shader: str = "height",
        *,
        debug_renderer: bool,
    ) -> None:
        self.draw_context = draw_context
        self.scale = scale
        self.relief_scale = relief_scale
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.color = 0
        self.shader = shader
        self.debug_renderer = debug_renderer

        self.tile: _Tile | None = None

    def render(self) -> None:
        """Render the tile."""
        if not self.tile:
            raise TypeError  # type guard for mypy

        outline = _DEBUG_OUTLINE_SHADE if self.debug_renderer else None
        width = _DEBUG_OUTLINE_WIDTH if self.debug_renderer else 0

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
            max_depth = math.sqrt(
                the_heightmap_size[0] ** 2 + the_heightmap_size[1] ** 2
            )
            depth = math.sqrt(self.tile.x**2 + self.tile.y**2)
            return normalise_8bit(depth, 0, max_depth)

        mean_height = sum(self.tile.vertex_heights) / 4
        return normalise_8bit(
            mean_height,
            heightmap_lowest(self.tile.heightmap),
            heightmap_highest(self.tile.heightmap),
        )
