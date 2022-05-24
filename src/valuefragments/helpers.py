"""helper functions and code snippets which are not decorators."""
import sys
from importlib.util import find_spec
from typing import IO, Protocol, TypedDict, TypeVar, Union

# https://github.com/microsoft/pyright/issues/3002#issuecomment-1046100462
from typing_extensions import Unpack

# found on https://stackoverflow.com/a/14981125


class Printable(Protocol):  # pylint: disable=too-few-public-methods
    """Typing Protocol for objects with __str__ method."""

    def __str__(self) -> str:
        ...


KwargsForPrint = TypedDict(
    "KwargsForPrint",
    {"sep": str, "end": str, "file": IO[str], "flush": bool},
    total=False,
)


def eprint(*args: Printable, **kwargs: Unpack[KwargsForPrint]) -> None:
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


FirstElementT = TypeVar("FirstElementT")
if __debug__ and find_spec("icecream"):
    from icecream import ic
else:

    def ic(  # pylint: disable=invalid-name
        *a: FirstElementT,
    ) -> Union[FirstElementT, tuple[FirstElementT, ...], None]:
        """Just in case package icecream is not available: For logging purposes."""
        if not a:
            return None
        return a[0] if len(a) == 1 else a


ic("a")
__all__ = ["eprint", "ic"]

try:
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    def backgroundme() -> None:
        """Give this process background priority."""
        if psutil.WINDOWS:
            try:
                # Details <https://archive.is/peWej#PROCESS_MODE_BACKGROUND_BEGIN>
                psutil.Process().nice(0x00100000)  # PROCESS_MODE_BACKGROUND_BEGIN
            except OSError as theerr:
                if theerr.winerror == 402:  # type: ignore # pylint: disable=no-member
                    ic("Prozess was already in background mode.")
                else:
                    print(theerr)
        else:
            psutil.Process().nice(19)

    __all__.append("backgroundme")


try:
    import hashlib
except ImportError:
    ic("hashlib is not available")
else:

    def hashfile(filename: str, chunklen: int = 128 * 2**12) -> str:
        """Return md5 hash for file."""
        with open(filename, "rb") as thefile:
            file_hash = hashlib.md5()  # nosec
            while chunk := thefile.read(chunklen):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    __all__.append("hashfile")


try:
    import cpu_load_generator
except ImportError:
    pass
else:

    def loadonecore(
        loadduration: int = 10, loadedcore: int = 0, theload: float = 0.5
    ) -> None:
        """Just a helper function to generate load on one given core."""
        cpu_load_generator.load_single_core(
            core_num=loadedcore,
            duration_s=loadduration,
            target_load=theload,
        )

    __all__.append("loadonecore")

    def loadallcores(loadduration: int = 10, theload: float = 0.5) -> None:
        """Just a helper function to generate load on all cores."""
        cpu_load_generator.load_all_cores(duration_s=loadduration, target_load=theload)

    __all__.append("loadallcores")
