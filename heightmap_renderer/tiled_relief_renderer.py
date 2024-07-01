"""TiledReliefRenderer class module."""

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
    ) -> None:
        """
        Parameters
        ----------
        heightmap
            Values must be >= 0.
        scale
            Scale factor to apply to the [TO DO image].
        """
        self.heightmap = heightmap
        self.lowest = heightmap_lowest(self.heightmap)
        self.highest = heightmap_highest(self.heightmap)

        the_heightmap_size = heightmap_size(self.heightmap)
        relief_height = self.highest - self.lowest

        self.image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=(
                round(the_heightmap_size[0] * SQRT_2)
                * scale,  # could use projection here
                the_heightmap_size[1] * scale,
            ),
        )
        draw_context = ImageDraw.Draw(self.image)

        for y in range(the_heightmap_size[0] - 1):
            for x in range(the_heightmap_size[1] - 1):
                tile = Tile(
                    x,
                    y,
                    heights=[
                        self.heightmap[x + dx][y + dy] for (dx, dy) in CORNER_OFFSETS
                    ],
                )
                tile_renderer = TileRenderer(
                    tile=tile,
                    draw_context=draw_context,
                    color=self.tile_shade(x, y),
                    scale=scale,
                    relief_scale=relief_scale,
                    x_offset=round(self.image.width / 2),
                    y_offset=relief_height * scale,
                )
                tile_renderer.render()

    def tile_shade(self, x: int, y: int) -> int:
        """Determine the tile colour (shade in current implementation)."""
        height = self.heightmap[x][y]
        shade = float(height)
        return normalise_8bit(shade, self.lowest, self.highest)

    def show(
        self,
    ) -> None:
        """Show the image."""
        self.image.show()
