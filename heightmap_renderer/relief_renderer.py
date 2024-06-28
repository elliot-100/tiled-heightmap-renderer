"""ReliefRenderer class module."""

from PIL import Image, ImageDraw
from PIL.Image import Resampling

from heightmap_renderer.utils import normalise_8bit


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
        self.lowest = min(min(row) for row in self.heightmap)
        self.highest = max(max(row) for row in self.heightmap)
        if self.lowest < 0:
            err_msg = "Heightmap values must be >= 0."
            raise ValueError(err_msg)
        self.value_range = self.highest - self.lowest

        heightmap_size = self.heightmap_size
        relief_height = relief_scale * self.value_range

        self.image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=(
                heightmap_size[0],
                heightmap_size[1] + relief_height,
            ),
        )
        draw = ImageDraw.Draw(self.image)

        for y in range(heightmap_size[0]):
            for x in range(heightmap_size[1]):
                draw.line(
                    (
                        (x, y + relief_height),
                        (x, y + relief_height - relief_scale * heightmap[x][y]),
                    ),
                    width=0,
                    fill=self.pixel_shade(x, y),
                )

        # draw extra 'front wall'
        y = heightmap_size[0] - 1
        for x in range(heightmap_size[1]):
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

    @property
    def heightmap_size(self) -> tuple[int, int]:
        """Get the size of the heightmap."""
        return len(self.heightmap), len(self.heightmap[0])

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
