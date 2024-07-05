"""TiledReliefRenderer class module."""

import math

from PIL import Image, ImageDraw

from heightmap_renderer._tile import _Tile
from heightmap_renderer._tile_renderer import _TileRenderer
from heightmap_renderer.utils import (
    _CORNER_OFFSETS,
    SQRT_2,
    heightmap_highest,
    heightmap_lowest,
    heightmap_size,
    normalise_8bit,
)


class TiledReliefRenderer:
    """Render a heightmap ...TO DO... with relief.

    Heightmap input initially implemented as simple Python array (list of list).

    NB: heights apply to vertices.
    """

    def __init__(
        self,
        heightmap: list[list[int]],
        scale: int = 1,
        relief_scale: float = 1,
        shader: str = "height",
        *,
        debug_renderer: bool = False,
    ) -> None:
        """
        Parameters
        ----------
        heightmap
            Values must be >= 0.
        scale
            Scale factor to apply to the [TO DO image].

        debug_renderer : bool
            If True, render 'debug' features, e.g. outlines.
            Defaults to False.
        """
        self.heightmap = heightmap
        self.scale = scale
        self.relief_scale = relief_scale
        self.shader = shader
        self.debug_renderer = debug_renderer

        self._lowest = heightmap_lowest(self.heightmap)
        self._highest = heightmap_highest(self.heightmap)

        self._heightmap_size = heightmap_size(self.heightmap)
        relief_height = self._highest - self._lowest

        self._image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=(
                round(self._heightmap_size[0] * SQRT_2)
                * scale,  # could use projection here
                self._heightmap_size[1] * scale,
            ),
        )
        self._draw_context = ImageDraw.Draw(self._image)
        self._x_offset = round(self._image.width / 2)
        self._y_offset = relief_height * scale
        self._render()

    def _render(self) -> None:
        for y in range(self._heightmap_size[0] - 1):
            for x in range(self._heightmap_size[1] - 1):
                heights = [
                    self.heightmap[x + dx][y + dy] for (dx, dy) in _CORNER_OFFSETS
                ]
                tile = _Tile(x, y, heights)
                tile_renderer = _TileRenderer(
                    tile=tile,
                    draw_context=self._draw_context,
                    color=self._tile_shade(tile),
                    scale=self.scale,
                    relief_scale=self.relief_scale,
                    x_offset=self._x_offset,
                    y_offset=self._y_offset,
                    debug_renderer=self.debug_renderer,
                )
                tile_renderer.render()

    def _tile_shade(self, tile: _Tile) -> int:
        """Determine the tile colour (shade in current implementation)."""
        if self.shader == "depth":
            max_depth = math.sqrt(
                self._heightmap_size[0] ** 2 + self._heightmap_size[1] ** 2
            )
            depth = math.sqrt(tile.x**2 + tile.y**2)
            return normalise_8bit(depth, 0, max_depth)

        mean_height = sum(tile.heights) / 4
        return normalise_8bit(mean_height, self._lowest, self._highest)

    def show(
        self,
    ) -> None:
        """Show the image."""
        self._image.show()
