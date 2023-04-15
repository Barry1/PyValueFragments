#!/usr/bin/env -S poetry run pytest
"""Test functions for helpers module."""
from .helpers import (  # pylint: disable=relative-beyond-top-level
    HumanReadAble,
    basic_auth,
    hashfile,
    pi_for_cpu_load,
    stringtovalidfilename,
)


def test_pi_for_cpu_load() -> None:
    """Check if pi calculation works in priciple."""
    assert pi_for_cpu_load(10, 4478) == 3.2
    assert pi_for_cpu_load(100, 4478) == 3.32
    assert pi_for_cpu_load(1000, 4478) == 3.176
    assert pi_for_cpu_load(10000, 4478) == 3.1276
    assert pi_for_cpu_load(100000, 4478) == 3.13836
    assert pi_for_cpu_load(1000000, 4478) == 3.140568
    assert pi_for_cpu_load(10000000, 4478) == 3.1413716
    assert pi_for_cpu_load(100000000, 4478) == 3.14188636
    assert pi_for_cpu_load(1000000000, 4478) == 3.14188636


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
