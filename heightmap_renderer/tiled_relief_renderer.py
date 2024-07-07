"""TiledReliefRenderer class module."""

from PIL import Image, ImageDraw

from heightmap_renderer._coordinate_int_2d import _CoordinateInt2D
from heightmap_renderer._tile import _Tile
from heightmap_renderer._tile_renderer import _TileRenderer
from heightmap_renderer.utils import (
    SQRT_2,
    heightmap_highest,
    heightmap_lowest,
    heightmap_size,
)


class TiledReliefRenderer:
    """Render a heightmap as a '2.5D' 8-bit greyscale image.

    Heights apply to vertices.
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
        Create a new TiledReliefRenderer instance.

        Parameters
        ----------
        heightmap
            Values must be >= 0
        scale
            Scale factor to apply to all dimensions
        relief_scale
            Additional z/height scale factor
        shader
            "height" (default) or
            "depth"
        debug_renderer
            True: draw extra features for debugging.
            Defaults to False
        """
        self.heightmap = heightmap
        """Initially implemented as simple Python array (list of list)."""
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
                round(self._heightmap_size.x * SQRT_2)
                * scale,  # could use projection here
                self._heightmap_size.y * scale,
            ),
        )
        self._draw_context = ImageDraw.Draw(self._image)
        self.offset = _CoordinateInt2D(
            round(self._image.width / 2), relief_height * scale
        )
        self._render()

    def _render(self) -> None:
        """Render the image."""
        tile_renderer = _TileRenderer(
            draw_context=self._draw_context,
            scale=self.scale,
            relief_scale=self.relief_scale,
            offset=self.offset,
            shader=self.shader,
            debug_renderer=self.debug_renderer,
        )
        for y in range(self._heightmap_size.x - 1):
            for x in range(self._heightmap_size.y - 1):
                self._render_tile(tile_renderer, _CoordinateInt2D(x, y))

    def _render_tile(
        self, tile_renderer: _TileRenderer, location: _CoordinateInt2D
    ) -> None:
        tile = _Tile(self.heightmap, location)
        tile_renderer.tile = tile
        tile_renderer.render()

    def show(
        self,
    ) -> None:
        """Show the image."""
        self._image.show()
