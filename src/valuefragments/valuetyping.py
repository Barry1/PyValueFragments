# valuetyping.py
"""Convenient re‑export of public typing‑symbols.

This module re‑exports the public names from ``typing`` and
``typing_extensions`` so they can be imported from a single place:

    from valuetyping import List, TypedDict, Any, ...

The implementation uses the modern __getattr__ + __dir__ pattern
→ perfect for type checkers and minimal runtime overhead.
"""

from __future__ import annotations

import typing as _typing
from types import ModuleType
from typing import IO, Any, TypedDict  # für KwargsForPrint + Typ-Hints

import typing_extensions as _typing_extensions


# ----------------------------------------------------------------------
# 1️⃣ Öffentliche Namen berechnen (genau wie vorher)
# ----------------------------------------------------------------------
def _public_names(module: ModuleType) -> set[str]:
    return {name for name in dir(module) if not name.startswith("_")}


_typing_names: set[str] = _public_names(module=_typing)
_typing_ext_names: set[str] = _public_names(module=_typing_extensions)

# Bevorzugt die stdlib-Version, wenn ein Name in beiden vorkommt
_all_names: list[str] = sorted(_typing_names | _typing_ext_names)


# ----------------------------------------------------------------------
# 2️⃣ Lazy Re-Export via __getattr__ (TypeChecker-freundlich)
# ----------------------------------------------------------------------
def __getattr__(name: str) -> Any:
    """Wird nur aufgerufen, wenn ein nicht-definiertes Attribut angefragt wird."""
    if name in _all_names:
        # Bevorzugt typing, sonst typing_extensions
        obj = (
            getattr(_typing, name)
            if hasattr(_typing, name)
            else getattr(_typing_extensions, name)
        )
        # Cachen im Modul-Namensraum (verhindert wiederholte Aufrufe)
        globals()[name] = obj
        return obj

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Öffentliche API für `from valuetyping import *` und IDE-Autocomplete
__all__ = _all_names


# ----------------------------------------------------------------------
# 3️⃣ Deine benutzerdefinierte TypedDict (ohne ignores)
# ----------------------------------------------------------------------
class KwargsForPrint(TypedDict, total=False):
    """Kwargs für print() – nur für Type Checking"""

    sep: str
    end: str
    file: IO[str]
    flush: bool


# Optional: __dir__ für vollständiges `dir(valuetyping)` und bessere IDE-Unterstützung
def __dir__() -> list[str]:
    """Alle öffentlichen Namen (inkl. der eigenen Klasse)."""
    return sorted(_all_names + ["KwargsForPrint"])
