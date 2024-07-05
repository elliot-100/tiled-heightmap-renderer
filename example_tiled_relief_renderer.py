"""Example script."""

from heightmap_renderer import EXAMPLE_HEIGHTMAP_32 as EXAMPLE_HEIGHTMAP
from heightmap_renderer.tiled_relief_renderer import TiledReliefRenderer

my_render = TiledReliefRenderer(
    heightmap=EXAMPLE_HEIGHTMAP,
    scale=32,
    relief_scale=1,
    shader="depth",
    debug_renderer=False,
)
my_render.show()
