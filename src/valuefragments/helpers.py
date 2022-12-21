"""helper functions and code snippets which are not decorators."""
from __future__ import annotations

# https://github.com/microsoft/pyright/issues/3002#issuecomment-1046100462
# found on https://stackoverflow.com/a/14981125
import asyncio
import concurrent.futures
import math
import os

# https://docs.python.org/3/library/__future__.html
import sys
from importlib.util import find_spec
from typing import (
    IO,
    TYPE_CHECKING,
    Callable,
    Generator,
    Protocol,
    Self,
    SupportsInt,
    TypedDict,
    TypeVar,
)

from typing_extensions import SupportsIndex, Unpack

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer, SupportsTrunc


def recurse_files_in_folder(thebasepath: str) -> Generator[str, None, None]:
    """return paths for all files in basepath recursively"""
    for root, _dirs, files in os.walk(thebasepath, topdown=False):
        for filename in files:
            yield os.path.join(root, filename)


class Printable(Protocol):  # pylint: disable=too-few-public-methods
    """Typing Protocol for objects with __str__ method."""

    def __str__(self) -> str:
        """Just the stringification."""
        ...  # pylint: disable=unnecessary-ellipsis


FirstElementT = TypeVar("FirstElementT")
_FunCallResultT = TypeVar("_FunCallResultT")
__all__: list[str] = []


class HumanReadAble(int):
    """int like with print in human readable scales."""

    # <https://pypi.python.org/pypi/humanize>
    def __new__(  # type: ignore[misc]
        cls,
        __x: str
        | ReadableBuffer
        | SupportsInt
        | SupportsIndex
        | SupportsTrunc,
        __baseunit: str = "B",
    ) -> Self:  # type: ignore[valid-type]
        """Build an int object by the super class."""
        return super().__new__(cls, __x)

    def __init__(
        self,
        __x: str
        | ReadableBuffer
        | SupportsInt
        | SupportsIndex
        | SupportsTrunc,
        __baseunit: str = "B",
    ) -> None:
        """Take int value, optional unit and prepare scaling."""
        self.unit: str = __baseunit
        #        self.scaler: int = math.floor(math.log2(self) / 10)
        #        self.scaler: int = math.floor(math.log10(self) / 3)
        self.scaler: int = (
            1 + math.floor(math.log2(self / 1000) / 10) if self > 0 else 0
        )
        super().__init__()

    def __format__(self, format_spec: str = ".3f") -> str:
        """Implement format-method human readable."""
        # <https://en.wikipedia.org/wiki/Binary_prefix#Specific_units_of_IEC_60027-2_A.2_and_ISO.2FIEC_80000>
        scalerdict: dict[int, str] = {
            1: "Ki",
            2: "Mi",
            3: "Gi",
            4: "Ti",
            5: "Pi",
            6: "Ei",
            7: "Zi",
            8: "Yi",
        }
        #        return '{val:{fmt}} {suf}'.format(val=val, fmt=format_spec, suf=suffix)
        return (
            f"{self / (1024 ** self.scaler):{format_spec}} "
            f'{scalerdict.get(self.scaler, "")}{self.unit}'
        )

    def __str__(self) -> str:
        """Show scaled readable value."""
        return self.__format__()

    def __repr__(self) -> str:
        """Show how to recreate object."""
        return f"{self.__class__.__name__}({super().__repr__()})"


__all__.append("HumanReadAble")
KwargsForPrint = TypedDict(
    "KwargsForPrint",
    {"sep": str, "end": str, "file": IO[str], "flush": bool},
    total=False,
)


async def to_inner_task(
    funcall: Callable[[None], _FunCallResultT],
    the_executor: concurrent.futures.Executor | None = None,
) -> _FunCallResultT:
    """Build FUTURE from funcall and convert to CORO."""
    return await asyncio.get_running_loop().run_in_executor(
        the_executor, funcall
    )


async def run_grouped_in_tpe(
    the_functioncalls: list[Callable[[None], _FunCallResultT]]
) -> list[_FunCallResultT]:
    """
    Run functions grouped (asyncio.TaskGroup) in ThreadPoolExecutor.

    as for now the functions needs to be without parameters, prepare your calls
    with functools.partial
    """
    with concurrent.futures.ThreadPoolExecutor() as pool_executor:
        async with asyncio.TaskGroup() as the_task_group:
            the_tasks: list[asyncio.Task[_FunCallResultT]] = [
                the_task_group.create_task(
                    to_inner_task(funcall, pool_executor)
                    #                    asyncio.to_thread(funcall)
                )
                for funcall in the_functioncalls
            ]
    return [ready_task.result() for ready_task in the_tasks]


__all__.append("run_grouped_in_tpe")


async def run_grouped_in_ppe(
    the_functioncalls: list[Callable[[None], _FunCallResultT]]
) -> list[_FunCallResultT]:
    """
    Run functions grouped (asyncio.TaskGroup) in ProcessPoolExecutor.

    as for now the functions needs to be without parameters, prepare your calls
    with functools.partial
    """
    with concurrent.futures.ProcessPoolExecutor() as pool_executor:
        async with asyncio.TaskGroup() as the_task_group:
            the_tasks: list[asyncio.Task[_FunCallResultT]] = [
                the_task_group.create_task(
                    to_inner_task(funcall, pool_executor)
                    #                    asyncio.to_thread(funcall)
                )
                for funcall in the_functioncalls
            ]
    return [ready_task.result() for ready_task in the_tasks]


__all__.append("run_grouped_in_ppe")


def eprint(*args: Printable, **_kwargs: Unpack[KwargsForPrint]) -> None:
    """Print to stderr and ignores kwargs."""
    print(*args, file=sys.stderr)


__all__.append("eprint")

if __debug__ and find_spec("icecream"):
    from icecream import ic
else:

    def ic(  # pylint: disable=invalid-name
        *a: FirstElementT,
    ) -> FirstElementT | tuple[FirstElementT, ...] | None:
        """Just in case icecream is not available: For logging purposes."""
        if not a:
            return None
        return a[0] if len(a) == 1 else a


__all__.append("ic")

try:
    # noinspection PyUnresolvedReferences
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    def backgroundme() -> None:
        """Give this process background priority."""
        if psutil.WINDOWS:
            try:
                # <https://archive.is/peWej#PROCESS_MODE_BACKGROUND_BEGIN>
                psutil.Process().nice(
                    0x00100000
                )  # PROCESS_MODE_BACKGROUND_BEGIN
            except OSError as theerr:
                if theerr.winerror == 402:  # type: ignore # pylint: disable=no-member
                    # pyright: ignore [reportGeneralTypeIssues,reportUnknownMemberType]
                    ic("Prozess was already in background mode.")
                else:
                    print(theerr)
        else:
            psutil.Process().nice(19)

    __all__.append("backgroundme")

try:
    # noinspection PyUnresolvedReferences
    import hashlib
except ImportError:
    ic("hashlib is not available")
else:

    def hashfile(filename: str, chunklen: int = 128 * 2**12) -> str:
        """Return md5 hash for file."""
        with open(filename, "rb") as thefile:
            file_hash: hashlib._Hash = (  # pyright: ignore[reportPrivateUsage]
                hashlib.md5()  # nosec  # Compliant
            )
            while chunk := thefile.read(chunklen):
                file_hash.update(chunk)
        # deepcode ignore InsecureHash: for file identification
        return file_hash.hexdigest()

    __all__.append("hashfile")

try:
    import cpu_load_generator  # pyright: ignore[reportUnknownVariableType]
except ImportError:
    pass
else:

    def loadonecore(
        loadduration: int = 10, loadedcore: int = 0, theload: float = 0.5
    ) -> None:
        """Generate load on one given core."""
        cpu_load_generator.load_single_core(  # pyright: ignore[reportUnknownMemberType]
            core_num=loadedcore,
            duration_s=loadduration,
            target_load=theload,
        )

    __all__.append("loadonecore")

    def loadallcores(loadduration: int = 10, theload: float = 0.5) -> None:
        """Just a helper function to generate load on all cores."""
        cpu_load_generator.load_all_cores(  # pyright: ignore[reportUnknownMemberType]
            duration_s=loadduration, target_load=theload
        )

    __all__.append("loadallcores")
