"""Utility functions."""


def normalise_8bit(value: float, lower_bound: int, upper_bound: int) -> int:
    """Normalise value to the range 0 <= n <= 255."""
    return int(255 * (value - lower_bound) / upper_bound - lower_bound)
