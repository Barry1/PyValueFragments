#!/usr/bin/env pytest
"""Test functions for helpers module."""
from .helpers import (  # pylint: disable=E0402  # pylint: disable=E0402
    HumanReadAble,
    basic_auth,
    hashfile,
)


def test_basic_auth() -> None:
    """PyTestMethod."""
    assert (
        basic_auth("Aladdin", "open sesame")[6:]
        == "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    )


def test_hashfile() -> None:
    """Pytest routine - md5sum of empty file."""
    assert hashfile("/dev/null") == "d41d8cd98f00b204e9800998ecf8427e"


def test_humanreadable() -> None:
    """Check if Calculation and units work."""
    assert format(HumanReadAble(2**10)) == "1.0 KiB"
    assert format(HumanReadAble(10**3)) == "0.9765625 KiB"
    assert format(HumanReadAble(2**20)) == "1.0 MiB"
    assert format(HumanReadAble(10**6, "baud")) == "976.5625 Kibaud"
    assert format(HumanReadAble(123456789), "10.2f") == "    117.74 MiB"
