# valuetyping.py
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
    from typing import ABCMeta
    from typing import AbstractSet
    from typing import Annotated
    from typing import Any
    from typing import AnyStr
    from typing import AsyncContextManager
    from typing import AsyncGenerator
    from typing import AsyncIterable
    from typing import AsyncIterator
    from typing import Awaitable
    from typing import BinaryIO
    from typing import ByteString
    from typing import CT_co
    from typing import Callable
    from typing import ChainMap
    from typing import ClassVar
    from typing import Collection
    from typing import Concatenate
    from typing import Container
    from typing import ContextManager
    from typing import Coroutine
    from typing import Counter
    from typing import DefaultDict
    from typing import Deque
    from typing import Dict
    from typing import EXCLUDED_ATTRIBUTES
    from typing import Final
    from typing import ForwardRef
    from typing import FrozenSet
    from typing import Generator
    from typing import Generic
    from typing import GenericAlias
    from typing import Hashable
    from typing import IO
    from typing import ItemsView
    from typing import Iterable
    from typing import Iterator
    from typing import KT
    from typing import KeysView
    from typing import List
    from typing import Literal
    from typing import LiteralString
    from typing import Mapping
    from typing import MappingView
    from typing import Match
    from typing import MutableMapping
    from typing import MutableSequence
    from typing import MutableSet
    from typing import NamedTuple
    from typing import NamedTupleMeta
    from typing import Never
    from typing import NewType
    from typing import NoDefault
    from typing import NoReturn
    from typing import NotRequired
    from typing import Optional
    from typing import OrderedDict
    from typing import ParamSpec
    from typing import ParamSpecArgs
    from typing import ParamSpecKwargs
    from typing import Pattern
    from typing import Protocol
    from typing import ReadOnly
    from typing import Required
    from typing import Reversible
    from typing import Self
    from typing import Sequence
    from typing import Set
    from typing import Sized
    from typing import SupportsAbs
    from typing import SupportsBytes
    from typing import SupportsComplex
    from typing import SupportsFloat
    from typing import SupportsIndex
    from typing import SupportsInt
    from typing import SupportsRound
    from typing import T
    from typing import TYPE_CHECKING
    from typing import T_co
    from typing import T_contra
    from typing import Text
    from typing import TextIO
    from typing import Tuple
    from typing import Type
    from typing import TypeAlias
    from typing import TypeAliasType
    from typing import TypeGuard
    from typing import TypeIs
    from typing import TypeVar
    from typing import TypeVarTuple
    from typing import TypedDict
    from typing import Union
    from typing import Unpack
    from typing import VT
    from typing import VT_co
    from typing import V_co
    from typing import ValuesView
    from typing import abstractmethod
    from typing import assert_never
    from typing import assert_type
    from typing import cast
    from typing import clear_overloads
    from typing import collections
    from typing import copyreg
    from typing import dataclass_transform
    from typing import defaultdict
    from typing import evaluate_forward_ref
    from typing import final
    from typing import functools
    from typing import get_args
    from typing import get_origin
    from typing import get_overloads
    from typing import get_protocol_members
    from typing import get_type_hints
    from typing import is_protocol
    from typing import is_typeddict
    from typing import no_type_check
    from typing import no_type_check_decorator
    from typing import operator
    from typing import overload
    from typing import override
    from typing import reveal_type
    from typing import runtime_checkable
    from typing import sys
    from typing import types

[
    "AbstractSet",
    "Annotated",
    "Any",
    "AnyStr",
    "AsyncContextManager",
    "AsyncGenerator",
    "AsyncIterable",
    "AsyncIterator",
    "Awaitable",
    "BinaryIO",
    "Buffer",
    "Callable",
    "CapsuleType",
    "ChainMap",
    "ClassVar",
    "Collection",
    "Concatenate",
    "Container",
    "ContextManager",
    "Coroutine",
    "Counter",
    "DefaultDict",
    "Deque",
    "Dict",
    "Doc",
    "Final",
    "Format",
    "ForwardRef",
    "FrozenSet",
    "Generator",
    "Generic",
    "GenericMeta",
    "Hashable",
    "IO",
    "IntVar",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KT",
    "KeysView",
    "List",
    "Literal",
    "LiteralString",
    "Mapping",
    "MappingView",
    "Match",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "NamedTuple",
    "Never",
    "NewType",
    "NoDefault",
    "NoExtraItems",
    "NoReturn",
    "NotRequired",
    "Optional",
    "OrderedDict",
    "PEP_560",
    "ParamSpec",
    "ParamSpecArgs",
    "ParamSpecKwargs",
    "Pattern",
    "Protocol",
    "ReadOnly",
    "Reader",
    "Required",
    "Reversible",
    "Self",
    "Sentinel",
    "Sequence",
    "Set",
    "Sized",
    "SupportsAbs",
    "SupportsBytes",
    "SupportsComplex",
    "SupportsFloat",
    "SupportsIndex",
    "SupportsInt",
    "SupportsRound",
    "T",
    "TYPE_CHECKING",
    "T_co",
    "T_contra",
    "Text",
    "TextIO",
    "Tuple",
    "Type",
    "TypeAlias",
    "TypeAliasType",
    "TypeForm",
    "TypeGuard",
    "TypeIs",
    "TypeVar",
    "TypeVarTuple",
    "TypedDict",
    "Union",
    "Unpack",
    "VT",
    "ValuesView",
    "Writer",
    "_ASSERT_NEVER_REPR_MAX_LENGTH",
    "_AnnotatedAlias",
    "_CapsuleType",
    "_ConcatenateGenericAlias",
    "_DefaultMixin",
    "_EXCLUDED_ATTRS",
    "_EllipsisDummy",
    "_ExtensionsSpecialForm",
    "_FORWARD_REF_HAS_CLASS",
    "_NEEDS_SINGLETONMETA",
    "_PEP_696_IMPLEMENTED",
    "_PEP_728_IMPLEMENTED",
    "_PROTO_ALLOWLIST",
    "_Sentinel",
    "_SpecialForm",
    "_TAKES_MODULE",
    "_TYPEDDICT_TYPES",
    "_TYPEVARTUPLE_TYPES",
    "_TypeFormForm",
    "_TypeVarLikeMeta",
    "_TypedDict",
    "_TypedDictMeta",
    "_TypedDictSpecialForm",
    "_UNPACK_DOC",
    "__all__",
    "__builtins__",
    "__cached__",
    "__doc__",
    "__file__",
    "__loader__",
    "__name__",
    "__package__",
    "__spec__",
    "_caller",
    "_check_generic",
    "_collect_parameters",
    "_concatenate_getitem",
    "_create_concatenate_alias",
    "_create_typeddict",
    "_get_protocol_attrs",
    "_get_typeddict_qualifiers",
    "_has_generic_or_protocol_as_origin",
    "_is_param_expr",
    "_is_unpack",
    "_is_unpacked_typevartuple",
    "_marker",
    "_overload_dummy",
    "_set_default",
    "_set_module",
    "_should_collect_from_parameters",
    "_types",
    "_typing_names",
    "_unpack_args",
    "abc",
    "annotationlib",
    "assert_never",
    "assert_type",
    "builtins",
    "cast",
    "clear_overloads",
    "collections",
    "contextlib",
    "dataclass_transform",
    "deprecated",
    "disjoint_base",
    "enum",
    "evaluate_forward_ref",
    "final",
    "functools",
    "get_annotations",
    "get_args",
    "get_origin",
    "get_original_bases",
    "get_overloads",
    "get_protocol_members",
    "get_type_hints",
    "inspect",
    "io",
    "is_protocol",
    "is_typeddict",
    "keyword",
    "no_type_check",
    "no_type_check_decorator",
    "operator",
    "overload",
    "override",
    "reveal_type",
    "runtime",
    "runtime_checkable",
    "sys",
    "type_repr",
    "typing",
    "warnings",
]
