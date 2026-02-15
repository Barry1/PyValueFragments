#!/usr/bin/env -S poetry run pytest
"""Test functions for mathhelpers module."""

from valuefragments.mathhelpers import (
    easybisect,
    loanrate,
    polyroot,
    probneeds,
    probneeds_rec,
)


def test_easybisect() -> None:
    """Check Bisection method."""
    [r1, r2] = easybisect(lambda x: x**x, 2, 3, 7)
    assert abs(r1 - 2.313017) < 1e-5
    assert abs(r2 - 6.955883) < 1e-5
    [r1, r2] = easybisect(lambda x: x**x, 2, 3, 7, maxiter=30, relerror=0.001)
    assert abs(r1 - 2.316117) < 1e-5
    assert abs(r2 - 6.995649) < 1e-5


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


def test_loanrate() -> None:
    """Check for loanrate calculation."""
    assert abs(loanrate(250000, 0.03, 15) - 1726.422852) < 1e-3
    assert abs(loanrate(250000, 0.035, 15) - 1787.1937256) < 1e-3
    assert abs(loanrate(250000, 0.035, 16) - 1702.355347) < 1e-3
    assert abs(loanrate(250000, 0.035, 17) - 1627.7401123) < 1e-3
    assert abs(loanrate(250000, 0.04, 15) - 1849.221069) < 1e-3
