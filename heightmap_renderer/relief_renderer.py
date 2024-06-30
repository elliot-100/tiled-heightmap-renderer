"""ReliefRenderer class module."""

from PIL import Image, ImageDraw
from PIL.Image import Resampling

from heightmap_renderer.utils import (
    heightmap_highest,
    heightmap_lowest,
    heightmap_size,
    normalise_8bit,
)


class ReliefRenderer:
    """Render a heightmap as an 8-bit greyscale image with relief.

    Heightmap input initially implemented as simple Python array (list of list).
    """

    def __init__(
        self,
        heightmap: list[list[int]],
        scale: int = 1,
        relief_scale: int = 1,
    ) -> None:
        """
        Parameters
        ----------
        heightmap
            Values must be >= 0.
        scale
            Scale factor to apply to the image.
        relief_scale
            Vertical scale factor
        """
        self.heightmap = heightmap
        self.lowest = heightmap_lowest(self.heightmap)
        self.highest = heightmap_highest(self.heightmap)

        the_heightmap_size = heightmap_size(self.heightmap)
        relief_height = self.highest - self.lowest

        self.image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=(
                the_heightmap_size[0],
                the_heightmap_size[1] + relief_height,
            ),
        )
        draw = ImageDraw.Draw(self.image)

        for y in range(the_heightmap_size[0]):
            for x in range(the_heightmap_size[1]):
                draw.line(
                    (
                        (x, y + relief_height),
                        (x, y + relief_height - relief_scale * heightmap[x][y]),
                    ),
                    width=0,
                    fill=self.pixel_shade(x, y),
                )

        # draw extra 'front wall'
        y = the_heightmap_size[0] - 1
        for x in range(the_heightmap_size[1]):
            # duplicate the last row in black,
            # 1 pixel lower, so it doesn't hide the real last row
            draw.line(
                (
                    (x, y + relief_height),
                    (x, y + relief_height - relief_scale * heightmap[x][y] + 1),
                ),
                width=0,
                fill=0,  # black
            )

        self.image = self.image.resize(
            size=(scale * self.image.size[0], scale * self.image.size[1]),
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
