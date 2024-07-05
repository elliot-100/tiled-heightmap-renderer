"""TiledReliefRenderer class module."""

import math

from PIL import Image, ImageDraw

from heightmap_renderer.tile import Tile
from heightmap_renderer.tile_renderer import TileRenderer
from heightmap_renderer.utils import (
    CORNER_OFFSETS,
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

        self.lowest = heightmap_lowest(self.heightmap)
        self.highest = heightmap_highest(self.heightmap)

        self.heightmap_size = heightmap_size(self.heightmap)
        relief_height = self.highest - self.lowest

        self.image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=(
                round(self.heightmap_size[0] * SQRT_2)
                * scale,  # could use projection here
                self.heightmap_size[1] * scale,
            ),
        )
        self.draw_context = ImageDraw.Draw(self.image)
        self.x_offset = round(self.image.width / 2)
        self.y_offset = relief_height * scale
        self._render()

    def _render(self) -> None:
        for y in range(self.heightmap_size[0] - 1):
            for x in range(self.heightmap_size[1] - 1):
                heights = [
                    self.heightmap[x + dx][y + dy] for (dx, dy) in CORNER_OFFSETS
                ]
                tile = Tile(x, y, heights)
                tile_renderer = TileRenderer(
                    tile=tile,
                    draw_context=self.draw_context,
                    color=self.tile_shade(tile),
                    scale=self.scale,
                    relief_scale=self.relief_scale,
                    x_offset=self.x_offset,
                    y_offset=self.y_offset,
                    debug_renderer=self.debug_renderer,
                )
                tile_renderer.render()

    def tile_shade(self, tile: Tile) -> int:
        """Determine the tile colour (shade in current implementation)."""
        if self.shader == "depth":
            max_depth = math.sqrt(
                self.heightmap_size[0] ** 2 + self.heightmap_size[1] ** 2
            )
            depth = math.sqrt(tile.x**2 + tile.y**2)
            return normalise_8bit(depth, 0, max_depth)

        mean_height = sum(tile.heights) / 4
        return normalise_8bit(mean_height, self.lowest, self.highest)

    def show(
        self,
    ) -> None:
        """Show the image."""
        self.image.show()
