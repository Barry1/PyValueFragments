# valuetyping.py
# pyright: reportUnusedImport=false, reportUnknownVariableType=false, reportAttributeAccessIssue=false
"""Convenient re‑export of public typing‑symbols.

This module re‑exports the public names from ``typing`` and
``typing_extensions`` so they can be imported from a single place:

    from valuetyping import List, TypedDict, Any, ...

The implementation uses the modern __getattr__ + __dir__ pattern
→ perfect for type checkers and minimal runtime overhead.
"""

from __future__ import annotations
import sys

if sys.version_info >= (3, 15):
    sys.set_lazy_imports("all")
if sys.version_info >= (3, 5, 3):
    from typing import ClassVar
else:
    from typing_extensions import ClassVar
if sys.version_info >= (3, 6, 2):
    from typing import NoReturn
else:
    from typing_extensions import NoReturn
if sys.version_info >= (3, 8):
    from typing import Literal
    from typing import Final
else:
    from typing_extensions import Concatenate
    from typing_extensions import Final
if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated
if sys.version_info >= (3, 10):
    from typing import Literal
    from typing import TypeGuard
else:
    from typing_extensions import Concatenate
    from typing_extensions import TypeGuard
if sys.version_info >= (3, 11):
    from typing import LiteralString
    from typing import Never
    from typing import Self
    from typing import Unpack
    from typing import Required, NotRequired
else:
    from typing_extensions import LiteralString
    from typing_extensions import Self
    from typing_extensions import Never
    from typing_extensions import Unpack
    from typing_extensions import Required, NotRequired
if sys.version_info >= (3, 13):
    from typing import ReadOnly
    from typing import TypeIs
else:
    from typing_extensions import ReadOnly
    from typing_extensions import TypeIs
import typing as _typing
from types import ModuleType
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    TypedDict,
)  # für KwargsForPrint + Typ-Hints

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


##########################################################################################################################################
if TYPE_CHECKING:
    # pyright: ignore[reportUnusedImport]
    # noqa: F401
    from typing import Any
