"""Example script."""

from heightmap_renderer import EXAMPLE_HEIGHTMAP_16
from heightmap_renderer.simple_renderer import SimpleRenderer

my_render = SimpleRenderer(heightmap=EXAMPLE_HEIGHTMAP_16, scale=32)
my_render.show()
