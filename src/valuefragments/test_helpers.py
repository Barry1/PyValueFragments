#!/usr/bin/env pytest
"""Test functions for helpers module."""
from .helpers import (  # pylint: disable=relative-beyond-top-level
    HumanReadAble,
    basic_auth,
    hashfile,
    stringtovalidfilename,
)


def test_stringtovalidfilename() -> None:
    """Test function for filename validity of strings."""
    assert (
        stringtovalidfilename("a:/xäü\\?*1__x&%&$§§)§(§/$<>-_,.;:;:)") == "axäü1__x§§)§(§-_,.;;)"
    )


def test_basic_auth() -> None:
    """Test if basic_auth does what is expected."""
    assert basic_auth("Aladdin", "open sesame")[6:] == "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="


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
