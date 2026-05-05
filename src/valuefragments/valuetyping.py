from types import ModuleType
from typing import TYPE_CHECKING, TypedDict, IO

if TYPE_CHECKING:
    # pyright: ignore[reportUnusedImport]
    # noqa: F401
    from typing import *
    from typing_extensions import *


class metatyping(type):
    _typingmodule = __import__("typing")
    _typing_extensionsmodule = __import__("typing_extensions")

    def __getattr__(self, name: str):
        if hasattr(self._typingmodule, name):
            setattr(self, name, getattr(self._typingmodule, name))
            return getattr(self._typingmodule, name)
        elif hasattr(self._typing_extensionsmodule, name):
            setattr(self, name, getattr(self._typing_extensionsmodule, name))
            return getattr(self._typing_extensionsmodule, name)
        else:
            raise AttributeError(f"{name!r} ist kein bekanntes Typ‑Alias")


class valuetyping(ModuleType, metaclass=metatyping):
    pass


def __getattr__(theattribute: str):
    return getattr(valuetyping, theattribute)


class KwargsForPrint(TypedDict, total=False):
    """Kwargs für print() – nur für Type Checking"""

    sep: str
    end: str
    file: IO[str]
    flush: bool
