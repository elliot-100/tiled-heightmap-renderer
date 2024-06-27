"""SimpleRenderer class module."""

from PIL import Image
from PIL.Image import Resampling


class SimpleRenderer:
    """Render a heightmap as an 8-bit greyscale image."""

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
        self.lowest = min(min(row) for row in self.heightmap)
        self.highest = max(max(row) for row in self.heightmap)
        if self.lowest < 0:
            err_msg = "Heightmap values must be >= 0."
            raise ValueError(err_msg)
        self.value_range = self.highest - self.lowest

        self.image = Image.new(
            mode="L",  # 8-bit pixels, grayscale
            size=self.heightmap_size,
        )
        pixel_data: list[int] = [
            self.pixel_shade(x, y)
            for x in range(
                self.heightmap_size[0],
            )
            for y in range(
                self.heightmap_size[1],
            )
        ]
        self.image.putdata(pixel_data)  # type: ignore[no-untyped-call]
        self.image = self.image.resize(
            size=(scale * self.heightmap_size[0], scale * self.heightmap_size[1]),
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
        return self._normalise_8bit(shade)

    def _normalise_8bit(self, value: float) -> int:
        """Normalise value to the range 0 <= n <= 255."""
        return int(value * 255 / self.value_range)

    def show(
        self,
    ) -> None:
        """Show the image."""
        self.image.show()
