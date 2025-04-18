#!/usr/bin/env -S poetry run pytest
"""Test functions for mathhelpers module."""

from .mathhelpers import easybisect, polyroot, probneeds, probneeds_rec


def test_easybisect() -> None:
    """Check Bisection method."""
    assert easybisect(lambda x: x**x, 2, 3, 7) == (2.3130177346728433, 6.955885095010905)
    assert easybisect(lambda x: x**x, 2, 3, 7, 30, 0.001) == (
        2.3161170287184474,
        6.995648896293349,
    )


def test_polyroot() -> None:
    """Check polynomial root calculation."""
    assert polyroot((1, 0, -1)) == (-1, 1)
    assert polyroot((1, -1, -2)) == (-1, 2)
    assert polyroot((1, -1, 0)) == (0, 1)
    assert polyroot((1, 0, 0)) == (0, 0)


def test_probneeds() -> None:
    """Check probability calculation for benoulli cases."""
    assert probneeds(needs=[3], probs=[0.6], avails=2) == 0.4
    assert probneeds(needs=[3], probs=[0.6], avails=3) == 1
    assert probneeds(needs=[], probs=[]) == 1
    assert probneeds(needs=[], probs=[], avails=4) == 1
    assert probneeds(needs=[2, 3], probs=[0.4, 0.6], avails=2) == 0.4
    assert probneeds(needs=[2, 3], probs=[0.4, 0.6], avails=3) == 0.76


def test_probneeds_rec() -> None:
    """Check probability calculation for benoulli cases."""
    assert probneeds_rec(needs=[3], probs=[0.6], avails=2) == 0.4
    assert probneeds_rec(needs=[3], probs=[0.6], avails=3) == 1
    assert probneeds_rec(needs=[], probs=[]) == 1
    assert probneeds_rec(needs=[], probs=[], avails=4) == 1
    assert probneeds_rec(needs=[2, 3], probs=[0.4, 0.6]) == 0.4
    assert probneeds_rec(needs=[2, 3], probs=[0.4, 0.6], avails=3) == 0.76
