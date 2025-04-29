# icecream.pyi is a stub file for icecream.py
# It is used to provide type hints for icecream.py
# icecream.pyi is not a part of the icecream package

from valuefragments.valuetyping import KwargsForPrint

def ic[
    *OthersT,
    LastT,
](  # pylint: disable=invalid-name
    *firsts: *OthersT, last: LastT | None = None, **_kwargs: KwargsForPrint
) -> (tuple[*OthersT, LastT] | LastT | None):
    """typing template"""
