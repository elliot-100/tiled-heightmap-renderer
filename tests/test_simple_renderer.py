"""Tests for SimpleRenderer class."""

from heightmap_renderer.simple_renderer import SimpleRenderer


def test_heightmap_size(sample_heightmap_16: list[list[int]]) -> None:
    """Test that heightmap size is determined correctly."""
    # arrange
    # act
    my_render = SimpleRenderer(
        heightmap=sample_heightmap_16,
    )
    # assert
    assert my_render.image.size == (16, 16)


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
