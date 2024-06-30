"""SimpleRenderer class module."""

from PIL import Image
from PIL.Image import Resampling

from heightmap_renderer.utils import (
    heightmap_highest,
    heightmap_lowest,
    heightmap_size,
    normalise_8bit,
)


class SimpleRenderer:
    """Render a heightmap as an 8-bit greyscale image.

    Heightmap input initially implemented as simple Python array (list of list).
    """

    def __init__(
        self,
        heightmap: list[list[int]],
        scale: int = 1,
    ) -> None:
        """
        Parameters
        ----------
        heightmap
            Values must be >= 0.
        scale
            Scale factor to apply to the image.
        """
        self.heightmap = heightmap
        self.lowest = heightmap_lowest(self.heightmap)
        self.highest = heightmap_highest(self.heightmap)

        the_heightmap_size = heightmap_size(self.heightmap)

        self.image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=the_heightmap_size,
        )
        pixel_data: list[int] = [
            self.pixel_shade(x, y)
            for x in range(
                the_heightmap_size[0],
            )
            for y in range(
                the_heightmap_size[1],
            )
        ]
        self.image.putdata(pixel_data)  # type: ignore[no-untyped-call]
        self.image = self.image.resize(
            size=(scale * the_heightmap_size[0], scale * the_heightmap_size[1]),
            resample=Resampling.NEAREST,
        )

    def pixel_shade(self, x: int, y: int) -> int:
        """Determine the pixel colour (shade in current implementation)."""
        height = self.heightmap[x][y]
        shade = float(height)
        return normalise_8bit(shade, self.lowest, self.highest)

    def show(
        self,
    ) -> None:
        """Show the image."""
        self.image.show()
