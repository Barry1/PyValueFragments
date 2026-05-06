from typing import IO, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import *  # pyright: ignore[reportWildcardImportFromLibrary]  # noqa: F403
    from typing_extensions import *  # pyright: ignore[reportWildcardImportFromLibrary]  # noqa: F403
_typingmodule = __import__("typing")
_typing_extensionsmodule = __import__("typing_extensions")


def _setattr(name, value):
    # 'globals()' bezieht sich hier auf das Modul selbst, simuliert __setattr__ auf Modulebene
    globals()[name] = value


def __getattr__(name: str):
    if hasattr(_typingmodule, name):
        _setattr(name, getattr(_typingmodule, name))
        return getattr(_typingmodule, name)
    if hasattr(_typing_extensionsmodule, name):
        _setattr(name, getattr(_typing_extensionsmodule, name))
        return getattr(_typing_extensionsmodule, name)
    raise AttributeError(f"{name!r} ist kein bekanntes Typ‑Alias")


class KwargsForPrint(TypedDict, total=False):
    """Kwargs für print() – nur für Type Checking"""

    sep: str
    end: str
    file: IO[str]
    flush: bool


def __dir__() -> list[str]:
    """Ermöglicht dir() auf Modulebene, Umleitung in die Klasse valuetyping und metaklasse metatyping."""
    return list(
        {"KwargsForPrint"}.union(dir(_typingmodule)).union(
            dir(_typing_extensionsmodule)
        )
    )
