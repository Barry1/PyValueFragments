#!/usr/bin/env pytest
"""Test functions for helpers module."""
from .helpers import hashfile  # pylint: disable=E0402


def test_hashfile() -> None:
    """Pytest routine - md5sum of empty file."""
    assert hashfile("/dev/null") == "d41d8cd98f00b204e9800998ecf8427e"
