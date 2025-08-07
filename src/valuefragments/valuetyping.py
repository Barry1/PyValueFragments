"""Module for typing information from typing and typing_extensions."""

# pylint: disable=wildcard-import,unused-wildcard-import
from typing import *  # type: ignore # noqa

from typing_extensions import *  # type: ignore # noqa


class KwargsForPrint(TypedDict, total=False):  # noqa: F405
    """Class for Type Checking Kwargs 2 Print"""

    sep: str
    end: str
    file: IO[str]  # noqa: F405
    flush: bool


# for python<=3.5,2.7
# https://typing.python.org/en/latest/...
# ...spec/typeddict.html#alternative-syntax
# KwargsForPrint = TypedDict(  # noqa: F405
#    "KwargsForPrint",
#    {"sep": str, "end": str, "file": IO[str], "flush": bool},  # noqa: F405
#    total=False,
# )
