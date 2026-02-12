"""Module for typing information from typing and typing_extensions."""

# pylint: disable=wildcard-import,unused-wildcard-import
import sys

__all__: list[str] = []


def importallfromtypingandtypingextensions() -> None:
    # This function is used to import all attributes from typing
    # and typing_extensions into the global namespace of the caller.
    # use instead of
    # from typing import *  # type: ignore # noqa
    # from typing_extensions import *  # type: ignore # noqa
    _typing = __import__(name="typing")
    _typing_extensions = __import__(name="typing_extensions")
    for singleattr in [
        item for item in dir(_typing) if not item.startswith("_")
    ]:
        # print(singleattr)
        sys._getframe(1).f_globals[singleattr] = getattr(
            __import__(name="typing"),
            singleattr,
        )
        sys._getframe(1).f_globals["__all__"].append(singleattr)
    #    for singleattr in [item for item in dir(_typing_extensions) if item not in dir(_typing)]:
    for singleattr in [
        item
        for item in dir(_typing_extensions)
        if item not in dir(_typing) and not item.startswith("_")
    ]:
        # print(singleattr)
        sys._getframe(1).f_globals[singleattr] = getattr(
            __import__(name="typing_extensions"),
            singleattr,
        )
        sys._getframe(1).f_globals["__all__"].append(singleattr)


importallfromtypingandtypingextensions()


class KwargsForPrint(TypedDict, total=False):  # type: ignore[name-defined,call-arg]  # noqa: F821
    """Class for Type Checking Kwargs 2 Print"""

    sep: str
    end: str
    file: IO[str]  # type: ignore[name-defined]  # noqa: F821
    flush: bool


# for python<=3.5,2.7
# https://typing.python.org/en/latest/...
# ...spec/typeddict.html#alternative-syntax
# KwargsForPrint = TypedDict(  # noqa: F405
#    "KwargsForPrint",
#    {"sep": str, "end": str, "file": IO[str], "flush": bool},  # noqa: F405
#    total=False,
# )
