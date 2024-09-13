"""Module for typing information from typing and typing_extensions."""

# pylint: disable=wildcard-import,unused-wildcard-import
from typing import *  # pyright: ignore[reportWildcardImportFromLibrary] # noqa: F401, F403

from typing_extensions import *  # type: ignore[no-redef,assignment] # noqa: F401, F403

# from typing import __all__ as typing_all


# from typing_extensions import __all__ as typing_extensions_all

# __all__: list[str] = [*typing_all, *typing_extensions_all]
