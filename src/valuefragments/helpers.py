"""helper functions and code snippets which are not decorators."""

from __future__ import annotations

from typing import Self

__all__: list[str] = []
import asyncio
import concurrent.futures
import hashlib
import logging
import math
import os
import random
import string
import sys
import time
from io import IOBase
from shutil import copyfileobj
from types import ModuleType

import requests

# noinspection PyProtectedMember
# pylint: disable-next=no-name-in-module
# pyright: ignore[reportAttributeAccessIssue,reportUnknownVariableType]
from lxml.html import fromstring

# https://docs.python.org/3/library/__future__.html
# https://github.com/microsoft/pyright/issues/3002#issuecomment-1046100462
# found on https://stackoverflow.com/a/14981125
from valuefragments.moduletools import moduleexport
from valuefragments.valuetyping import (  # LastElementT,; OtherElementsT,; SupportsAbs,; TypeVar,
    IO,
    TYPE_CHECKING,
    Callable,
    Generator,
    Literal,
    Protocol,
    SupportsIndex,
    SupportsInt,
    TypedDict,
    reveal_type,
)

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer, SupportsTrunc
thelogger: logging.Logger = logging.getLogger(__name__)


class Printable(Protocol):  # pylint: disable=too-few-public-methods
    """Typing Protocol for objects with __str__ method."""

    def __str__(self: Printable) -> str:
        """Just the stringification."""
        ...  # pylint: disable=unnecessary-ellipsis


# _FunCallResultT = TypeVar("_FunCallResultT")


@moduleexport
def int2bin(number: int, digits: int) -> str:
    """string with binary represantation of number without 0b"""
    # following <https://stackoverflow.com/a/75668709>
    return f"{number:b}".zfill(digits)

    # return bin(number)[2:].zfill(digits)
    # return f'{number:0{digits}b}'


@moduleexport
def file_exists_current(filepathname: str, max_age_seconds: int = 60 * 60 * 24 * 7) -> bool:
    """Check if given file exists and is not older than max_age_seconds."""
    return (
        os.path.exists(filepathname)
        and time.time() - os.path.getmtime(filepathname) < max_age_seconds
    )


@moduleexport
def filecache[_FunCallResultT](
    filepathname: str,
    genupdmeth: Callable[[], IOBase],
    procmeth: Callable[[str], _FunCallResultT],
    max_age_seconds: int = 60 * 60 * 24 * 7,
) -> _FunCallResultT:
    """Check if cachefile exists and current. Updates if neccesary. Returns processed content."""
    if not file_exists_current(filepathname, max_age_seconds):
        with open(filepathname, "wb") as thefile:
            with genupdmeth() as thesrc:
                copyfileobj(thesrc, thefile)
        thelogger.info("File %s refreshed.", filepathname)
    return procmeth(filepathname)


@moduleexport
def thread_native_id_filter(record: logging.LogRecord) -> bool:
    """Inject thread_id to log records"""
    setattr(record, "thread_native", __import__("threading").get_native_id())
    return True


@moduleexport
def pi_for_cpu_load(
    numiter: int = 10**7, theseed: None | int | float | str | bytes | bytearray = None
) -> float:
    """Calculate pi by simulation just for CPU-load."""
    random.seed(theseed)
    n_all: int = 0
    n_in: int = 0
    for _ in range(numiter):
        _x: float = random.uniform(0, 1)
        _y: float = random.uniform(0, 1)
        n_all += 1
        if _x**2 + _y**2 < 1:
            n_in += 1
    return 4 * n_in / n_all


@moduleexport
def recurse_files_in_folder(thebasepath: str) -> Generator[str, None, None]:
    """Recursivly return paths for all files in basepath."""
    for root, _dirs, files in os.walk(thebasepath, topdown=False):
        for filename in files:
            yield os.path.join(root, filename)


@moduleexport
def basic_auth(
    user: str,
    passw: str,
) -> str:
    """Build String for Basic AUTH."""
    # Authorization token: we need to base 64 encode (utf-8) it
    # and then decode it to acsii as python 3 stores it as a byte string
    return "Basic " + __import__("base64").b64encode(f"{user}:{passw}".encode()).decode("ascii")


@moduleexport
class HumanReadAble(int):
    """int like with print in human readable scales."""

    # <https://pypi.python.org/pypi/humanize>
    # <https://typing.python.org/en/latest/spec/constructors.html#new-method>
    def __new__(
        cls,
        __x: ReadableBuffer | str | SupportsInt | SupportsIndex | SupportsTrunc,
        __baseunit: str = "B",
    ) -> Self:
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
            f"{self / (1024**self.scaler):{format_spec}} "
            f"{scalerdict.get(self.scaler, '')}{self.unit}"
        )

    def __str__(self) -> str:
        """Show scaled readable value."""
        return self.__format__()

    def __repr__(self) -> str:
        """Show how to recreate object."""
        return f"{self.__class__.__name__}({super().__repr__()})"


KwargsForPrint = TypedDict(
    "KwargsForPrint",
    {"sep": str, "end": str, "file": IO[str], "flush": bool},
    total=False,
)


@moduleexport
def closeifrunningloky() -> None:
    """Check if any (loky) backend is still open and if, close."""
    try:
        # pylint: disable=import-outside-toplevel
        from joblib.externals.loky.reusable_executor import get_reusable_executor
    except ModuleNotFoundError:
        pass
    else:
        get_reusable_executor().shutdown()


async def to_inner_task[_FunCallResultT](
    funcall: Callable[[], _FunCallResultT],
    the_executor: concurrent.futures.Executor | None = None,
) -> _FunCallResultT:
    """Build FUTURE from funcall and convert to CORO."""
    return await asyncio.get_running_loop().run_in_executor(executor=the_executor, func=funcall)


@moduleexport
def eprint(*args: Printable, **_kwargs: KwargsForPrint) -> None:
    """Print to stderr and ignores kwargs."""
    print(*args, file=sys.stderr)


@moduleexport
def exists_variable(varname: str) -> bool:
    """Check if variable is in use - global or local."""
    return varname in globals() or varname in locals()


try:
    # from icecream import ic # type: ignore[attr-defined]
    # ic=__import__("icecream").ic
    ic = __import__("icecream").icecream.IceCreamDebugger()
except ImportError:
    # <https://stackoverflow.com/a/73738408>
    # pylint: disable-next=keyword-arg-before-vararg
    #    def ic(  # pylint: disable=invalid-name
    #        *firsts: *OtherElementsT, last: LastElementT | None = None, **_kwargs: KwargsForPrint
    #    ) -> tuple[*OtherElementsT, LastElementT] | LastElementT | None:
    def ic[*OthersT, LastT](
        *firsts: *OthersT, last: LastT | None = None, **_kwargs: KwargsForPrint
    ) -> tuple[*OthersT, LastT] | LastT | None:
        """Just in case icecream is not available: For logging purposes."""
        return (*firsts, last) if last and firsts else last

else:
    module: ModuleType = sys.modules["valuefragments.helpers"]
    if hasattr(module, "__all__"):
        if "ic" not in module.__all__:
            module.__all__.append("ic")
    else:
        setattr(module, "__all__", ["ic"])
finally:
    __all__.append("ic")


try:
    # noinspection PyUnresolvedReferences
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    @moduleexport
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


@moduleexport
def hashfile(filename: str, chunklen: int = 128 * 2**12) -> str:
    """Return md5 hash for file."""
    with open(filename, "rb") as thefile:
        # nosec  # Compliant
        file_hash = hashlib.md5(usedforsecurity=False)
        while chunk := thefile.read(chunklen):
            file_hash.update(chunk)
    # deepcode ignore InsecureHash: for file identification
    return file_hash.hexdigest()


try:
    # noinspection PyUnresolvedReferences
    from cpu_load_generator import load_all_cores, load_single_core
except ImportError:
    pass
else:

    @moduleexport
    def loadonecore(loadduration: int = 10, loadedcore: int = 0, theload: float = 0.5) -> None:
        """Generate load on one given core."""
        load_single_core(
            core_num=loadedcore,
            duration_s=loadduration,
            target_load=theload,
        )

    @moduleexport
    def loadallcores(loadduration: int = 10, theload: float = 0.5) -> None:
        """Just a helper function to generate load on all cores."""
        load_all_cores(duration_s=loadduration, target_load=theload)


@moduleexport
def stringtovalidfilename(inputstring: str) -> str:
    """Return only valid characters of string for use in filenames.

    easy solution by exclusion of maybe strange or forbidden characters
    <https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file#:~:text=Use%20any%20character,does%20not%20allow.>
    """
    return "".join(thechar for thechar in inputstring if thechar not in '<>&:"\\/|?*%$')


@moduleexport
def stringtovalidfilename2(inputstring: str) -> str:
    """Return only valid characters of string for use in filenames."""

    return "".join(
        thechar
        for thechar in inputstring
        if thechar in f"-_.{string.ascii_letters}{string.digits}"
    )


if sys.version_info >= (3, 11):
    HowType = Literal["tpe", "ppe", "thread"]

    @moduleexport
    async def run_grouped[_FunCallResultT](
        the_functioncalls: list[Callable[[], _FunCallResultT]],
        how: HowType = "thread",
    ) -> list[_FunCallResultT]:
        """Execute funcalls async by given method."""
        match how:
            case "thread":
                async with asyncio.TaskGroup() as the_task_group:
                    all_tasks: list[asyncio.Task[_FunCallResultT]] = [
                        the_task_group.create_task(asyncio.to_thread(funcall))
                        for funcall in the_functioncalls
                    ]
                return [ready_task.result() for ready_task in all_tasks]
            case "ppe":
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    async with asyncio.TaskGroup() as the_task_group:
                        all_tasks = [
                            the_task_group.create_task(to_inner_task(funcall, executor))
                            for funcall in the_functioncalls
                        ]
                return [ready_task.result() for ready_task in all_tasks]
            case "tpe":
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    async with asyncio.TaskGroup() as the_task_group:
                        all_tasks = [
                            the_task_group.create_task(to_inner_task(funcall, executor))
                            for funcall in the_functioncalls
                        ]
                return [ready_task.result() for ready_task in all_tasks]
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                print("how was '", how, "' but needs to be one of {'thread','tpe','ppe'}.")
                raise NotImplementedError(
                    "how was '", how, "' but needs to be one of {'thread','tpe','ppe'}."
                )


@moduleexport
def getselectedhreflinks(
    thebaseurl: str = "https://www.goc-stuttgart.de/event-guide/ergebnisarchiv",
    thesubstring: str = "fileadmin/ergebnisse/2024",
    thetimeout: int | tuple[int, int] = (5, 10),
) -> list[str]:
    """Parse HTML from URL for anachor-tag href matches by XPATH"""
    # <https://devhints.io/xpath> <https://stackoverflow.com/q/78877951>
    try:
        thesourcehtml: requests.Response = requests.get(url=thebaseurl, timeout=thetimeout)
    except requests.exceptions.Timeout:
        thelogger.error("timeout exception while fetching %s", thebaseurl)
        return []
    # Connect Timeout 5s, 10s for transmission
    thelogger.debug(
        "Request to %s with Status %i and Reason %s",
        thebaseurl,
        thesourcehtml.status_code,
        thesourcehtml.reason,
    )
    return reveal_type(
        fromstring(html=thesourcehtml.content).xpath(
            f'//a/@href[contains(string(), "{thesubstring}")]'
        )
    )
