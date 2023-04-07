#!/usr/bin/env -S poetry run pytest
"""Test functions for decorators module."""

import time

from .decorators import memoize  # pylint: disable=relative-beyond-top-level


def test_memoize() -> None:
    """Pytest routine - memoize for sleep of empty file."""
    memsleep = memoize(time.sleep)
    start = time.monotonic()
    memsleep(1)
    assert time.monotonic() >= 1 + start
    start = time.monotonic()
    memsleep(1)
    assert time.monotonic() < start + 1e-4
