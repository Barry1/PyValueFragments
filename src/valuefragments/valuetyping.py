"""Module for typing information from typing and typing_extensions."""

# pylint: disable=wildcard-import,unused-wildcard-import
from typing import *  # pyright: ignore[reportWildcardImportFromLibrary] # noqa: F401, F403

from typing_extensions import *  # type: ignore[no-redef,assignment] # noqa: F401, F403

LastElementT = TypeVar("LastElementT")  # noqa: F405
OtherElementsT = TypeVarTuple("OtherElementsT")  # noqa: F405
KwargsForPrint = TypedDict(  # noqa: F405
    "KwargsForPrint",
    {"sep": str, "end": str, "file": IO[str], "flush": bool},  # noqa: F405
    total=False,
)
