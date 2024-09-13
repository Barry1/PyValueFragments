"""Just a module for tools around module usage."""

from __future__ import annotations

import sys
from types import ModuleType

from .valuetyping import Callable, ParamSpec, TypeVar

# from .helpers import ic
_FunCallResultT = TypeVar("_FunCallResultT")
_FunParamT = ParamSpec("_FunParamT")


def moduleexport(
    class_or_function: Callable[_FunParamT, _FunCallResultT],
) -> Callable[_FunParamT, _FunCallResultT]:
    """Adds function or class magical to module's __all__."""
    # Following the idea from <https://stackoverflow.com/a/35710527/#:~:text=export%20decorator>
    module: ModuleType = sys.modules[class_or_function.__module__]
    # ic(class_or_function.__name__ + " in " + class_or_function.__module__)
    # ic(dir(module))
    if hasattr(module, "__all__"):
        if class_or_function.__name__ not in module.__all__:
            module.__all__.append(class_or_function.__name__)
    else:
        setattr(module, "__all__", [class_or_function.__name__])
    # ic(dir(module))
    # ic(module)
    # ic(module.__all__)
    return class_or_function
