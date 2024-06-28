"""Example script."""

from heightmap_renderer import EXAMPLE_HEIGHTMAP_32 as EXAMPLE_HEIGHTMAP
from heightmap_renderer.simple_renderer import SimpleRenderer

my_render = SimpleRenderer(heightmap=EXAMPLE_HEIGHTMAP, scale=32)
my_render.show()
