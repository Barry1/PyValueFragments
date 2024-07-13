#!/usr/bin/env -S poetry run pytest
"""Test functions for helpers module."""
from .helpers import (  # pylint: disable=relative-beyond-top-level
    HumanReadAble,
    basic_auth,
    easybisect,
    file_exists_current,
    hashfile,
    int2bin,
    pi_for_cpu_load,
    stringtovalidfilename,
)

# from .decorators import logdecorate


def test_file_actual_current() -> None:
    assert not file_exists_current("/ThisFileWillNeverExist.SURE")
    assert file_exists_current("/", 100 * 366 * 24 * 60 * 60)


# @logdecorate


def test_pi_for_cpu_load() -> None:
    """Check if pi calculation works in priciple."""
    assert pi_for_cpu_load(10, 4478) == 3.2
    assert pi_for_cpu_load(100, 4478) == 3.32
    assert pi_for_cpu_load(1000, 4478) == 3.176
    assert pi_for_cpu_load(10000, 4478) == 3.1276
    assert pi_for_cpu_load(100000, 4478) == 3.13836
    assert pi_for_cpu_load(1000000, 4478) == 3.140568
    # 1.04 seconds to here
    # assert pi_for_cpu_load(10000000, 4478) == 3.1413716
    # 10.23 seconds to here
    # assert pi_for_cpu_load(100000000, 4478) == 3.14188636
    # assert pi_for_cpu_load(1000000000, 4478) == 3.141731728


def test_int2bin() -> None:
    """Check binary representations of numbers and digits."""
    assert int2bin(5, 8) == "00000101"
    assert int2bin(5, 7) == "0000101"
    assert int2bin(5, 6) == "000101"
    assert int2bin(5, 5) == "00101"
    assert int2bin(4478, 14) == "01000101111110"
    assert int2bin(4478, 13) == "1000101111110"
    assert int2bin(4478, 12) == "1000101111110"


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


def test_easybisect() -> None:
    """Check Bisection method."""
    assert easybisect(lambda x: x**x, 2, 3, 7) == (2.3130177346728433, 6.955885095010905)
    assert easybisect(lambda x: x**x, 2, 3, 7, 30, 0.001) == (
        2.3161170287184474,
        6.995648896293349,
    )
