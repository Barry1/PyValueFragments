#!/usr/bin/env -S poetry run pytest
"""Test functions for mathhelpers module."""
from .mathhelpers import easybisect


def test_easybisect() -> None:
    """Check Bisection method."""
    assert easybisect(lambda x: x**x, 2, 3, 7) == (2.3130177346728433, 6.955885095010905)
    assert easybisect(lambda x: x**x, 2, 3, 7, 30, 0.001) == (
        2.3161170287184474,
        6.995648896293349,
    )
