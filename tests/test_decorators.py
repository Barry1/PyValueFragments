#!/usr/bin/env -S poetry run pytest
"""Test functions for decorators module."""

__lazy_modules__: list[str] = ["time", "valuefragments.decorators"]
import time

from valuefragments.decorators import (
    memoize,  # pylint: disable=relative-beyond-top-level
)


def test_memoize() -> None:
    """Pytest routine - memoize for sleep of empty file."""
    memsleep = memoize(time.sleep)
    start = time.monotonic()
    memsleep(1)
    assert time.monotonic() >= 1 + start
    start = time.monotonic()
    memsleep(1)
    assert time.monotonic() < start + 1e-4
