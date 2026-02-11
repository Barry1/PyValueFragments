"""Module for typing information from typing and typing_extensions."""

# pylint: disable=wildcard-import,unused-wildcard-import
from typing import *  # type: ignore # noqa

from typing_extensions import *  # type: ignore # noqa

# Preparation without StarImports


def typing_or_typing_extensions_import(modulename: str):
    try:
        globals().update(
            {modulename: getattr(__import__(name="typing"), modulename)}
        )
    except (ImportError, AttributeError):
        try:
            globals().update(
                {
                    modulename: getattr(
                        __import__(name="typing_extensions"),
                        modulename,
                    )
                }
            )
        except (ImportError, AttributeError):
            print(
                f"{modulename} is not available in typing or typing_extensions. Please upgrade to Python 3.8+ or install typing_extensions."
            )


needed: list[str] = ["Sentinel", "TypedDict", "IO"]
for neededel in needed:
    typing_or_typing_extensions_import(neededel)


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
