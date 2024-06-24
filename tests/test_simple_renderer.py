"""Tests for SimpleRenderer class."""

from heightmap_renderer.simple_renderer import SimpleRenderer


def test_heightmap_size(sample_heightmap: list[list[int]]) -> None:
    """Test that heightmap size is determined correctly."""
    # arrange
    # act
    my_render = SimpleRenderer(
        heightmap=sample_heightmap,
    )
    # assert
    assert my_render.heightmap_size == (14, 17)


def test_normalise() -> None:
    """Test that image pixel values are determined correctly."""
    my_heightmap = [
        [0, 1],
        [1, 2],
    ]
    # act
    my_render = SimpleRenderer(
        heightmap=my_heightmap,
    )
    pixels = list(my_render.image.getdata())
    # assert
    assert pixels == [0, 127, 127, 255]
