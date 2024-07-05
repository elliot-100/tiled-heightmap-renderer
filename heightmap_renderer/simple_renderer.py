"""SimpleRenderer class module."""

from PIL import Image

from heightmap_renderer.utils import (
    heightmap_highest,
    heightmap_lowest,
    heightmap_size,
    normalise_8bit,
)


class SimpleRenderer:
    """Render a heightmap as a 2D 8-bit greyscale image.

    Heights apply to pixel centres.
    """

    def __init__(
        self,
        heightmap: list[list[int]],
        scale: int = 1,
    ) -> None:
        """Create a new SimpleRenderer instance.

        Parameters
        ----------
        heightmap
            Values must be >= 0
        scale
            Scale factor to apply
        """
        self.heightmap = heightmap
        """Initially implemented as simple Python array (list of list)."""
        self._lowest = heightmap_lowest(self.heightmap)
        self._highest = heightmap_highest(self.heightmap)

        the_heightmap_size = heightmap_size(self.heightmap)

        self._image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=the_heightmap_size,
        )
        pixel_data: list[int] = [
            self._pixel_shade(x, y)
            for x in range(
                the_heightmap_size[0],
            )
            for y in range(
                the_heightmap_size[1],
            )
        ]
        self._image.putdata(pixel_data)  # type: ignore[no-untyped-call]
        self._image = self._image.resize(
            size=(scale * the_heightmap_size[0], scale * the_heightmap_size[1]),
            resample=Image.Resampling.NEAREST,
        )

    def _pixel_shade(self, x: int, y: int) -> int:
        """Determine the pixel colour (shade in current implementation)."""
        height = self.heightmap[x][y]
        shade = float(height)
        return normalise_8bit(shade, self._lowest, self._highest)

    def show(
        self,
    ) -> None:
        """Show the image."""
        self._image.show()
