"""helper functions and code snippets which are not decorators."""

from __future__ import annotations

__all__: list[str] = []

from asyncio import Task as asyncio_Task
from asyncio import TaskGroup as asyncio_TaskGroup
from asyncio import get_running_loop as asyncio_get_running_loop
from asyncio import to_thread as asyncio_to_thread
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
from io import IOBase
from logging import DEBUG as logging_DEBUG
from logging import INFO as logging_INFO
from logging import FileHandler as logging_FileHandler
from logging import Formatter as logging_Formatter
from logging import Logger as logging_Logger
from logging import LogRecord as logging_LogRecord
from logging import getLogger as logging_getLogger
from math import floor, log2
from os import getpid as os_getpid
from os import path as os_path
from os import walk as os_walk
from shutil import copyfileobj
from string import ascii_letters, digits
from types import ModuleType
from warnings import warn

from requests import Response as requests_Response
from requests import exceptions as requests_exceptions
from requests import get as requests_get

from .moduletools import moduleexport
from .valuetyping import (
    IO,
    Any,
    Callable,  # LastElementT,; OtherElementsT,
    Generator,
    Literal,
    Protocol,
    SupportsAbs,
    TypedDict,
    TypeVar,
    reveal_type,
)

_LAZY_IMPORTS: dict[str, str] = {
    "my_heavy_function": "submodule.heavy_processing",
    "another_function": "submodule.utils",
}

Tinput = TypeVar("Tinput")
Toutput = TypeVar("Toutput", bound=SupportsAbs[Any])
thelogger: logging_Logger = logging_getLogger(__name__)


class Printable(Protocol):  # pylint: disable=too-few-public-methods
    """Typing Protocol for objects with __str__ method."""

    def __str__(self: Printable) -> str:
        """Just the stringification."""
        ...  # pylint: disable=unnecessary-ellipsis


_FunCallResultT = TypeVar("_FunCallResultT")


@moduleexport
def int2bin(number: int, digits: int) -> str:
    """string with binary represantation of number without 0b"""
    # following <https://stackoverflow.com/a/75668709>
    return f"{number:b}".zfill(digits)

    # return bin(number)[2:].zfill(digits)
    # return f'{number:0{digits}b}'


@moduleexport
def file_exists_current(
    filepathname: str, max_age_seconds: int = 60 * 60 * 24 * 7
) -> bool:
    """Check if given file exists and is not older than max_age_seconds."""
    from time import time  # pylint: disable=import-outside-toplevel

    return (
        os_path.exists(filepathname)
        and time() - os_path.getmtime(filepathname) < max_age_seconds
    )


@moduleexport
def filecache(
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
def thread_native_id_filter(record: logging_LogRecord) -> bool:
    """Inject thread_id to log records"""
    record.thread_native = __import__("threading").get_native_id()  # pylint: disable=import-outside-toplevel
    return True


@moduleexport
def pi_for_cpu_load(
    numiter: int = 10**7, theseed: None | int | float | str | bytes | bytearray = None
) -> float:
    """Calculate pi by simulation just for CPU-load."""
    from random import seed, uniform  # pylint: disable=import-outside-toplevel

    seed(theseed)
    n_all: int = 0
    n_in: int = 0
    for _ in range(numiter):
        _x: float = uniform(0, 1)
        _y: float = uniform(0, 1)
        n_all += 1
        if _x**2 + _y**2 < 1:
            n_in += 1
    return 4 * n_in / n_all


@moduleexport
def recurse_files_in_folder(thebasepath: str) -> Generator[str, None, None]:
    """Recursivly return paths for all files in basepath."""
    for root, _dirs, files in os_walk(thebasepath, topdown=False):
        for filename in files:
            yield os_path.join(root, filename)


@moduleexport
def basic_auth(
    user: str,
    passw: str,
) -> str:
    """Build String for Basic AUTH."""
    # Authorization token: we need to base 64 encode it
    # and then decode it to acsii as python 3 stores it as a byte string
    return "Basic " + __import__("base64").b64encode(  # pylint: disable=import-outside-toplevel
        f"{user}:{passw}".encode("utf-8")
    ).decode("ascii")


@moduleexport
class HumanReadAble(int):
    """int like with print in human readable scales."""

    # if TYPE_CHECKING:  # _typesched only available in type checking context
    #    from _typeshed import (  # pylint: disable=import-outside-toplevel
    #        ReadableBuffer,
    #        SupportsTrunc,
    #    )

    # <https://pypi.python.org/pypi/humanize>
    def __new__(
        cls,
        __x,  #: ReadableBuffer | str | SupportsInt | SupportsIndex | SupportsTrunc,
        __baseunit: str = "B",
    ) -> HumanReadAble:
        """Build an int object by the super class."""
        return super().__new__(cls, __x)

    def __init__(
        self,
        __x,  #: str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc,
        __baseunit: str = "B",
    ) -> None:
        """Take int value, optional unit and prepare scaling."""
        self.unit: str = __baseunit
        #        self.scaler: int = math.floor(math.log2(self) / 10)
        #        self.scaler: int = math.floor(math.log10(self) / 3)
        self.scaler: int = 1 + floor(log2(self / 1000) / 10) if self > 0 else 0
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
        from joblib.externals.loky import get_reusable_executor  # type: ignore
    except ModuleNotFoundError:
        pass
    else:
        get_reusable_executor().shutdown()


async def to_inner_task(
    funcall: Callable[[], _FunCallResultT],
    the_executor: Executor | None = None,
) -> _FunCallResultT:
    """Build FUTURE from funcall and convert to CORO."""
    return await asyncio_get_running_loop().run_in_executor(the_executor, funcall)


@moduleexport
def eprint(*args: Printable, **_kwargs: KwargsForPrint) -> None:
    """Print to stderr and ignores kwargs."""
    from sys import stderr  # pylint: disable=import-outside-toplevel

    print(*args, file=stderr)


@moduleexport
def exists_variable(varname: str) -> bool:
    """Check if variable is in use - global or local."""
    return varname in globals() or varname in locals()


try:
    from icecream import ic  # pylint: disable=import-outside-toplevel
except ImportError:
    # <https://stackoverflow.com/a/73738408>
    # pylint: disable-next=keyword-arg-before-vararg
    #    def ic(  # pylint: disable=invalid-name
    #        *firsts: *OtherElementsT, last: LastElementT | None = None, **_kwargs: KwargsForPrint
    #    ) -> tuple[*OtherElementsT, LastElementT] | LastElementT | None:
    def ic(*firsts: Any, last: Any = None, **_kwargs: KwargsForPrint) -> Any:
        """Just in case icecream is not available: For logging purposes."""
        return (*firsts, last) if last and firsts else last

else:
    from sys import modules as sys_modules  # pylint: disable=import-outside-toplevel

    module: ModuleType = sys_modules["valuefragments.helpers"]
    if hasattr(module, "__all__"):
        if "ic" not in module.__all__:
            module.__all__.append("ic")
    else:
        module.__all__ = ["ic"]
finally:
    __all__.append("ic")


try:
    # noinspection PyUnresolvedReferences
    import psutil  # pylint: disable=import-outside-toplevel
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
    from _hashlib import HASH  # pylint: disable=import-outside-toplevel
    from hashlib import file_digest  # pylint: disable=import-outside-toplevel

    with open(filename, "rb") as thefile:
        # nosec  # Compliant
        file_hash: HASH = file_digest(thefile, "md5")
    # deepcode ignore InsecureHash: for file identification
    return file_hash.hexdigest()


try:
    # noinspection PyUnresolvedReferences
    from cpu_load_generator import (  # pylint: disable=import-outside-toplevel
        load_all_cores,
        load_single_core,
    )
except ImportError:
    pass
else:

    @moduleexport
    def loadonecore(
        loadduration: int = 10, loadedcore: int = 0, theload: float = 0.5
    ) -> None:
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
        thechar for thechar in inputstring if thechar in f"-_.{ascii_letters}{digits}"
    )


HowType = Literal["tpe", "ppe", "thread"]


@moduleexport
async def run_grouped(
    the_functioncalls: list[Callable[[], _FunCallResultT]],
    how: HowType = "thread",
) -> list[_FunCallResultT]:
    """Execute funcalls async by given method."""
    match how:
        case "thread":
            async with asyncio_TaskGroup() as the_task_group:
                all_tasks: list[asyncio_Task[_FunCallResultT]] = [
                    the_task_group.create_task(asyncio_to_thread(funcall))
                    for funcall in the_functioncalls
                ]
            return [ready_task.result() for ready_task in all_tasks]
        case "ppe":
            with ProcessPoolExecutor() as executor:
                async with asyncio_TaskGroup() as the_task_group:
                    all_tasks = [
                        the_task_group.create_task(to_inner_task(funcall, executor))
                        for funcall in the_functioncalls
                    ]
            return [ready_task.result() for ready_task in all_tasks]
        case "tpe":
            with ThreadPoolExecutor() as executor:
                async with asyncio_TaskGroup() as the_task_group:
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
async def run_calls_in_executor(
    the_functioncalls: list[Callable[[], _FunCallResultT]],
    the_executor: Executor,
) -> list[asyncio_Task[_FunCallResultT]]:
    """place functioncalls in given executor"""
    warn(
        "Will be removed from v0.4 on, use valuefragments.run_grouped",
        DeprecationWarning,
        stacklevel=2,
    )
    async with asyncio_TaskGroup() as the_task_group:
        return [
            the_task_group.create_task(to_inner_task(funcall, the_executor))
            for funcall in the_functioncalls
        ]


async def run_grouped_in_tpe(
    the_functioncalls: list[Callable[[], _FunCallResultT]],
) -> list[_FunCallResultT]:
    """
    Run functions grouped (asyncio_TaskGroup) in ThreadPoolExecutor.

    as for now the functions needs to be without parameters, prepare your calls
    with functools.partial
    """
    warn(
        "Will be removed from v0.4 on, use valuefragments.run_grouped",
        DeprecationWarning,
        stacklevel=2,
    )
    with ThreadPoolExecutor() as pool_executor:
        return [
            ready_task.result()
            for ready_task in await run_calls_in_executor(
                the_functioncalls, pool_executor
            )
        ]


async def run_grouped_in_ppe(
    the_functioncalls: list[Callable[[], _FunCallResultT]],
) -> list[_FunCallResultT]:
    """
    Run functions grouped (asyncio_TaskGroup) in ProcessPoolExecutor.

    as for now the functions needs to be without parameters, prepare your calls
    with functools.partial
    """
    warn(
        "Will be removed from v0.4 on, use valuefragments.run_grouped",
        DeprecationWarning,
        stacklevel=2,
    )
    with ProcessPoolExecutor() as pool_executor:
        return [
            ready_task.result()
            for ready_task in await run_calls_in_executor(
                the_functioncalls, pool_executor
            )
        ]


@moduleexport
def getselectedhreflinks(
    thebaseurl: str = "https://www.goc-stuttgart.de/event-guide/ergebnisarchiv",
    thesubstring: str = "fileadmin/ergebnisse/2024",
    thetimeout: int | tuple[int, int] = (5, 10),
) -> list[str]:
    """Parse HTML from URL for anachor-tag href matches by XPATH"""
    # <https://devhints.io/xpath> <https://stackoverflow.com/q/78877951>
    try:
        thesourcehtml: requests_Response = requests_get(
            url=thebaseurl, timeout=thetimeout
        )
    except requests_exceptions.Timeout:
        thelogger.error("timeout exception while fetching %s", thebaseurl)
        return []
    # Connect Timeout 5s, 10s for transmission
    thelogger.debug(
        "Request to %s with Status %i and Reason %s",
        thebaseurl,
        thesourcehtml.status_code,
        thesourcehtml.reason,
    )
    from lxml.html import fromstring  # pylint: disable=import-outside-toplevel
    return reveal_type(
        fromstring(html=thesourcehtml.content).xpath(
            f'//a/@href[contains(string(), "{thesubstring}")]'
        )
    )


def print_time_result(wall: float, user: float, system: float) -> None:
    """Print Time Result."""
    print(
        f"{wall:8.3f} [s]",
        f"(User: {user:8.3f} [s]",
        "System: {system:8.3f} [s])",
        f"{100 * (user + system) / wall:6.2f}% Load",
        sep="\t",
    )


@moduleexport
def setuplogger(LOGGERNAME: str) -> logging_Logger:
    """Setup Logging environment."""
    thelogger: logging_Logger = logging_getLogger(LOGGERNAME)
    # https://docs.python.org/3/library/logging_html#logrecord-attributes
    if not thelogger.hasHandlers():
        logformatter: logging_Formatter = logging_Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logfilehandler: logging_FileHandler = logging_FileHandler(f"{LOGGERNAME}.log")
        logfilehandler.setFormatter(logformatter)
        thelogger.addHandler(logfilehandler)
        if __debug__:
            thelogger.setLevel(logging_DEBUG)
        else:
            thelogger.setLevel(logging_INFO)
        # thelogger.log(logging_INFO,thelogger.getEffectiveLevel())
        thelogger.info(
            "Logging handler configured in process %i / thread %i",
            os_getpid(),
            # get_native_id(),
            __import__("threading").get_native_id(),  # pylint: disable=import-outside-toplevel
        )
        thelogger.debug("%s", __import__("traceback").format_stack())
    return thelogger
