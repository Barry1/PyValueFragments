"""Module for typing information from typing and typing_extensions."""

# pylint: disable=wildcard-import,unused-wildcard-import
from typing import *  # type: ignore # noqa

from typing_extensions import *  # type: ignore # noqa

# Example without StarImports

try:
    # Sentinel=__import__(name="typing", fromlist="Sentinel").Sentinel
    # from typing import Sentinel
    globals().update(
        {
            "Sentinel": getattr(
                __import__(name="typing", fromlist="Sentinel"), "Sentinel"
            )
        }
    )
except (ImportError, AttributeError):
    # Sentinel=__import__(name="typing_extensions", fromlist="Sentinel").Sentinel
    try:
        globals().update(
            {
                "Sentinel": getattr(
                    __import__(name="typing_extensions", fromlist="Sentinel"),
                    "Sentinel",
                )
            }
        )
    except (ImportError, AttributeError):
        print(
            "Sentinel is not available in typing or typing_extensions. Please upgrade to Python 3.8+ or install typing_extensions."
        )
# globals().update({"Sentinel":getattr(__import__(name="typing_extensions", fromlist="Sentinel"),"Sentinel")})


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
