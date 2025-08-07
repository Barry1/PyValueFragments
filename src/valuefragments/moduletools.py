"""Just a module for tools around module usage."""

from __future__ import annotations

from types import ModuleType

from .valuetyping import Callable

# from .helpers import ic
# _FunCallResultT = TypeVar("_FunCallResultT")
# _fun_param_t = ParamSpec("_fun_param_t")
# replaced by Type parameter lists
# <https://docs.python.org/3/reference/compound_stmts.html#type-parameter-lists>


def moduleexport[_FunCallResultT, **_fun_param_t](
    class_or_function: Callable[_fun_param_t, _FunCallResultT],
) -> Callable[_fun_param_t, _FunCallResultT]:
    """Adds function or class magical to module's __all__."""
    # Following the idea from
    # <https://stackoverflow.com/a/35710527/#:~:text=export%20decorator>
    module: ModuleType = __import__(name="sys").modules[
        class_or_function.__module__
    ]
    if hasattr(module, "__all__"):
        if class_or_function.__name__ not in module.__all__:
            module.__all__.append(class_or_function.__name__)
    else:
        setattr(module, "__all__", [class_or_function.__name__])
    # ic(dir(module))
    # ic(module)
    # ic(module.__all__)
    return class_or_function
