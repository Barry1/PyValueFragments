from typing import TypeVar, TypedDict

from typing_extensions import TypeVarTuple, Unpack

LastElementT = TypeVar("LastElementT")
OtherElementsT = TypeVarTuple("OtherElementsT")
KwargsForPrint = TypedDict(
    "KwargsForPrint",
    {"sep": str, "end": str, "file": IO[str], "flush": bool},
    total=False,
)

def ic(  # pylint: disable=invalid-name
    *rest: Unpack[OtherElementsT], last: LastElementT | None = None, **_kwargs: KwargsForPrint
) -> tuple[Unpack[OtherElementsT], LastElementT] | LastElementT | None:
    """typing template"""
