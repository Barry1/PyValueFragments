# valuetyping.py
"""Convenient re‑export of public typing‑symbols.

This module purposefully re‑exports the public names from ``typing`` and
``typing_extensions`` so they can be imported from a single place:
`from valuetyping import List, TypedDict, ...`

The implementation avoids fiddling with ``globals()`` and ``sys._getframe``.
"""

from __future__ import annotations

import typing as _typing
from types import ModuleType
from typing import IO, TypedDict  # needed for the TypedDict below

import typing_extensions as _typing_extensions


# ----------------------------------------------------------------------
# 1️⃣ Build the public name whitelist (everything that does *not* start
#    with an underscore and is present in either module).
# ----------------------------------------------------------------------
def _public_names(module: ModuleType) -> set[str]:
    return {name for name in dir(module) if not name.startswith("_")}


_typing_names: set[str] = _public_names(module=_typing)
_typing_ext_names: set[str] = _public_names(module=_typing_extensions)

# Merge, preferring the std‑library version when a name exists in both.
_all_names: list[str] = sorted(_typing_names | _typing_ext_names)

# Populate the module globals *once*.
globals().update(
    {
        name: (
            getattr(
                _typing,
                name,
            )
            if hasattr(_typing, name)
            else getattr(_typing_extensions, name)
        )
        for name in _all_names
    }
)

# Export the public API.
__all__: list[str] = list(_all_names)


class KwargsForPrint(TypedDict, total=False):  # type: ignore[name-defined,call-arg]  # noqa: F821
    """Class for Type Checking Kwargs 2 Print"""

    sep: str
    end: str
    file: IO[str]  # type: ignore[name-defined]  # noqa: F821
    flush: bool
