"""Just a module for tools around module usage."""

from __future__ import annotations

from types import ModuleType

from .valuetyping import Callable, ParamSpec, TypeVar

_FunCallResultT = TypeVar("_FunCallResultT")
_FunParamT = ParamSpec("_FunParamT")


def moduleexport(
    class_or_function: Callable[_FunParamT, _FunCallResultT],
) -> Callable[_FunParamT, _FunCallResultT]:
    """Adds function or class magical to module's __all__."""
    module: ModuleType = __import__("sys").modules[class_or_function.__module__]
    if hasattr(module, "__all__"):
        if class_or_function.__name__ not in module.__all__:
            module.__all__.append(class_or_function.__name__)
    else:
        setattr(module, "__all__", [class_or_function.__name__])
    return class_or_function
