"""Fixtures for pytest."""

import pytest

from heightmap_renderer import EXAMPLE_HEIGHTMAP


@pytest.fixture()
def sample_heightmap() -> list[list[int]]:
    """Return a sample heightmap."""
    return EXAMPLE_HEIGHTMAP
