from types import ModuleType
from typing import IO, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import *  #  pyright: ignore[reportUnusedImport,reportWildcardImportFromLibrary] # noqa: F401,F403

    from typing_extensions import *  #  pyright: ignore[reportUnusedImport,reportWildcardImportFromLibrary] # noqa: F401,F403


class metatyping(type):
    _typingmodule = __import__("typing")
    _typing_extensionsmodule = __import__("typing_extensions")

    def __getattr__(self, name: str):
        if hasattr(self._typingmodule, name):
            setattr(self, name, getattr(self._typingmodule, name))
            return getattr(self._typingmodule, name)
        if hasattr(self._typing_extensionsmodule, name):
            setattr(self, name, getattr(self._typing_extensionsmodule, name))
            return getattr(self._typing_extensionsmodule, name)
        raise AttributeError(f"{name!r} ist kein bekanntes Typ‑Alias")


class valuetyping(ModuleType, metaclass=metatyping):
    pass


def __getattr__(theattribute: str):
    """Ermöglicht Imports auf Modulebene, Umleitung in die Klasse valuetyping und metaklasse metatyping."""
    return getattr(valuetyping, theattribute)


class KwargsForPrint(TypedDict, total=False):
    """Kwargs für print() – nur für Type Checking"""

    sep: str
    end: str
    file: IO[str]
    flush: bool
