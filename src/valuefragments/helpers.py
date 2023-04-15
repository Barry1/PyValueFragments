"""helper functions and code snippets which are not decorators."""
from __future__ import annotations

# https://docs.python.org/3/library/__future__.html
# https://github.com/microsoft/pyright/issues/3002#issuecomment-1046100462
# found on https://stackoverflow.com/a/14981125
import asyncio
import concurrent.futures
import math
import os
import random
import string
import sys
import threading
import warnings
from base64 import b64encode
from importlib.util import find_spec
from typing import (
    IO,
    TYPE_CHECKING,
    Callable,
    Generator,
    Literal,
    Protocol,
    SupportsInt,
    TypedDict,
    TypeVar,
)

from typing_extensions import SupportsIndex, TypeVarTuple  # Self,

if sys.version_info < (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack  # pylint: disable=no-name-in-module

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer, SupportsTrunc


class Printable(Protocol):  # pylint: disable=too-few-public-methods
    """Typing Protocol for objects with __str__ method."""

    def __str__(self: Printable) -> str:
        """Just the stringification."""
        ...  # pylint: disable=unnecessary-ellipsis


FirstElementT = TypeVar("FirstElementT")
OtherElementsT = TypeVarTuple("OtherElementsT")


_FunCallResultT = TypeVar("_FunCallResultT")
__all__: list[str] = []


def thread_native_id_filter(record: _FunCallResultT) -> _FunCallResultT:
    """Inject thread_id to log records"""
    record.thread_native: int = threading.get_native_id()
    return record


__all__.append("thread_native_id_filter")


def pi_for_cpu_load(
    numiter: int = 10**7, theseed: None | int | float | str | bytes | bytearray = None
) -> float:
    """Calculate pi by simulation just for CPU-load."""
    random.seed(theseed)
    n: int = 0
    n_in: int = 0
    for _ in range(numiter):
        x: float = random.uniform(0, 1)
        y: float = random.uniform(0, 1)
        n += 1
        if x**2 + y**2 < 1:
            n_in += 1
    return 4 * n_in / n


__all__.append("pi_for_cpu_load")


def recurse_files_in_folder(thebasepath: str) -> Generator[str, None, None]:
    """Recursivly return paths for all files in basepath."""
    for root, _dirs, files in os.walk(thebasepath, topdown=False):
        for filename in files:
            yield os.path.join(root, filename)


__all__.append("recurse_files_in_folder")


def basic_auth(
    user: str,
    passw: str,
) -> str:
    """Build String for Basic AUTH."""
    # Authorization token: we need to base 64 encode it
    # and then decode it to acsii as python 3 stores it as a byte string
    return "Basic " + b64encode(f"{user}:{passw}".encode("utf-8")).decode("ascii")


__all__.append("basic_auth")


class HumanReadAble(int):
    """int like with print in human readable scales."""

    # <https://pypi.python.org/pypi/humanize>
    def __new__(
        cls,
        __x: ReadableBuffer | str | SupportsInt | SupportsIndex | SupportsTrunc,
        __baseunit: str = "B",
    ) -> HumanReadAble:
        """Build an int object by the super class."""
        return super().__new__(cls, __x)

    def __init__(
        self,
        __x: str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc,
        __baseunit: str = "B",
    ) -> None:
        """Take int value, optional unit and prepare scaling."""
        self.unit: str = __baseunit
        #        self.scaler: int = math.floor(math.log2(self) / 10)
        #        self.scaler: int = math.floor(math.log10(self) / 3)
        self.scaler: int = 1 + math.floor(math.log2(self / 1000) / 10) if self > 0 else 0
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
    return await asyncio.get_running_loop().run_in_executor(the_executor, funcall)


if sys.version_info >= (3, 11):

    async def run_grouped(
        the_functioncalls: list[Callable[[None], _FunCallResultT]],
        how: Literal["tpe", "ppe", "thread"] = "thread",
    ) -> list[_FunCallResultT]:
        """Execute funcalls async by given method."""
        if how == "thread":
            async with asyncio.TaskGroup() as the_task_group:
                all_tasks = [
                    the_task_group.create_task(asyncio.to_thread(funcall))
                    for funcall in the_functioncalls
                ]
            return [ready_task.result() for ready_task in all_tasks]
        if how == "ppe":
            with concurrent.futures.ProcessPoolExecutor() as executor:
                async with asyncio.TaskGroup() as the_task_group:
                    all_tasks = [
                        the_task_group.create_task(to_inner_task(funcall, executor))
                        for funcall in the_functioncalls
                    ]
            return [ready_task.result() for ready_task in all_tasks]
        if how == "tpe":
            with concurrent.futures.ThreadPoolExecutor() as executor:
                async with asyncio.TaskGroup() as the_task_group:
                    all_tasks = [
                        the_task_group.create_task(to_inner_task(funcall, executor))
                        for funcall in the_functioncalls
                    ]
            return [ready_task.result() for ready_task in all_tasks]
        print("how was '", how, "' but needs to be one of {'thread','tpe','ppe'}.")
        raise NotImplementedError(
            "how was '", how, "' but needs to be one of {'thread','tpe','ppe'}."
        )

    __all__.append("run_grouped")

    ######################################
    async def run_calls_in_executor(
        the_functioncalls: list[Callable[[None], _FunCallResultT]], the_executor
    ) -> list[asyncio.Task[_FunCallResultT]]:
        """place functioncalls in given executor"""
        warnings.warn(
            "Will be removed from v0.4 on, use valuefragments.run_grouped", DeprecationWarning
        )
        async with asyncio.TaskGroup() as the_task_group:
            return [
                the_task_group.create_task(to_inner_task(funcall, the_executor))
                for funcall in the_functioncalls
            ]

    __all__.append("run_calls_in_executor")

    async def run_grouped_in_tpe(
        the_functioncalls: list[Callable[[None], _FunCallResultT]]
    ) -> list[_FunCallResultT]:
        """
        Run functions grouped (asyncio.TaskGroup) in ThreadPoolExecutor.

        as for now the functions needs to be without parameters, prepare your calls
        with functools.partial
        """
        warnings.warn(
            "Will be removed from v0.4 on, use valuefragments.run_grouped", DeprecationWarning
        )
        with concurrent.futures.ThreadPoolExecutor() as pool_executor:
            return [
                ready_task.result()
                for ready_task in await run_calls_in_executor(the_functioncalls, pool_executor)
            ]

    __all__.append("run_grouped_in_tpe")

    async def run_grouped_in_ppe(
        the_functioncalls: list[Callable[[None], _FunCallResultT]]
    ) -> list[_FunCallResultT]:
        """
        Run functions grouped (asyncio.TaskGroup) in ProcessPoolExecutor.

        as for now the functions needs to be without parameters, prepare your calls
        with functools.partial
        """
        warnings.warn(
            "Will be removed from v0.4 on, use valuefragments.run_grouped", DeprecationWarning
        )
        with concurrent.futures.ProcessPoolExecutor() as pool_executor:
            return [
                ready_task.result()
                for ready_task in run_calls_in_executor(the_functioncalls, pool_executor)
            ]

    __all__.append("run_grouped_in_ppe")


def eprint(*args: Printable, **_kwargs: KwargsForPrint) -> None:
    """Print to stderr and ignores kwargs."""
    print(*args, file=sys.stderr)


__all__.append("eprint")

if __debug__ and find_spec("icecream"):
    from icecream import ic
else:

    def ic(
        first: FirstElementT | None = None, *rest: Unpack[OtherElementsT]
    ) -> FirstElementT | tuple[FirstElementT, Unpack[OtherElementsT]] | None:
        """Just in case icecream is not available: For logging purposes."""
        return (first, *rest) if first and rest else first


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
                psutil.Process().nice(0x00100000)  # PROCESS_MODE_BACKGROUND_BEGIN
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
            # nosec  # Compliant
            file_hash: hashlib._hashlib.HASH = hashlib.md5()
            while chunk := thefile.read(chunklen):
                file_hash.update(chunk)
        # deepcode ignore InsecureHash: for file identification
        return file_hash.hexdigest()

    __all__.append("hashfile")

try:
    # noinspection PyUnresolvedReferences
    from cpu_load_generator import (  # type: ignore[attr-defined]
        load_all_cores,
        load_single_core,
    )
except ImportError:
    pass
else:

    def loadonecore(loadduration: int = 10, loadedcore: int = 0, theload: float = 0.5) -> None:
        """Generate load on one given core."""
        load_single_core(
            core_num=loadedcore,
            duration_s=loadduration,
            target_load=theload,
        )

    __all__.append("loadonecore")

    def loadallcores(loadduration: int = 10, theload: float = 0.5) -> None:
        """Just a helper function to generate load on all cores."""
        load_all_cores(duration_s=loadduration, target_load=theload)

    __all__.append("loadallcores")


def stringtovalidfilename(inputstring: str) -> str:
    """Return only valid characters of string for use in filenames.

    easy solution by exclusion of maybe strange or forbidden characters
    <https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file#:~:text=Use%20any%20character,does%20not%20allow.>
    """
    return "".join(thechar for thechar in inputstring if thechar not in '<>&:"\\/|?*%$')


__all__.append("stringtovalidfilename")


def stringtovalidfilename2(inputstring: str) -> str:
    """Return only valid characters of string for use in filenames."""

    return "".join(
        thechar
        for thechar in inputstring
        if thechar in f"-_.{string.ascii_letters}{string.digits}"
    )


__all__.append("stringtovalidfilename2")
