# icecream.pyi is a stub file for icecream.py
# It is used to provide type hints for icecream.py
# icecream.pyi is not a part of the icecream package

from valuefragments.valuetyping import LastElementT, OtherElementsT, KwargsForPrint

def ic(  # pylint: disable=invalid-name
    *firsts: *OtherElementsT, last: LastElementT | None = None, **_kwargs: KwargsForPrint
) -> tuple[*OtherElementsT, LastElementT] | LastElementT | None:
    """typing template"""
