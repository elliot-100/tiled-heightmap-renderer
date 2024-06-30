"""Example script."""

from heightmap_renderer import EXAMPLE_HEIGHTMAP_32 as EXAMPLE_HEIGHTMAP
from heightmap_renderer.relief_renderer import ReliefRenderer

my_render = ReliefRenderer(heightmap=EXAMPLE_HEIGHTMAP, scale=32)
my_render.show()
