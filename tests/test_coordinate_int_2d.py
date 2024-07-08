"""Tests for CoordinateInt2D class."""

from heightmap_renderer._coordinate_int_2d import _CoordinateInt2D


def test_add() -> None:
    """Test that two coordinates can be added together."""
    # arrange
    a = _CoordinateInt2D(4, 5)
    b = _CoordinateInt2D(13, 2)

    # act
    c = a + b
    # assert
    assert c == _CoordinateInt2D(17, 7)


def test_multiply_by_int() -> None:
    """Test that a coordinate can be multiplied by an int."""
    # arrange
    a = _CoordinateInt2D(7, 6)
    b = 3

    # act
    c = a * b
    # assert
    assert c == _CoordinateInt2D(21, 18)
