"""Fixtures for pytest."""

import pytest

from heightmap_renderer import EXAMPLE_HEIGHTMAP_16


@pytest.fixture()
def sample_heightmap_16() -> list[list[int]]:
    """Return a sample heightmap."""
    return EXAMPLE_HEIGHTMAP_16
