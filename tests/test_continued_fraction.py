#!/usr/bin/env -S poetry run pytest
"""Test functions for mathhelpers module."""

import math

from valuefragments.continued_fraction import continued_fraction


def test_continued_fraction_int() -> None:
    """Test continued_fraction function."""
    for i in range(1, 10):
        assert continued_fraction(i) == [i]


def test_continued_fraction_fraction() -> None:
    """Test continued_fraction function."""
    assert continued_fraction(1 / 345) == [0, 345]
    for i in range(1, 10):
        assert continued_fraction(1 / 2**i) == [0, 2**i]


def test_continued_fraction() -> None:
    """Test continued_fraction function."""
    assert continued_fraction(math.pi) == [3, 7, 15, 1, 292, 1, 1, 1]
    assert continued_fraction(math.e) == [2, 1, 2, 1, 1, 4, 1, 1]
    assert continued_fraction(math.sqrt(2)) == [1, 2, 2, 2, 2, 2, 2, 2]
