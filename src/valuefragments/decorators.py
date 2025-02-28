"""module holding decorators."""

from __future__ import annotations

import logging
import os
import time
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable

# typing with the help of
# <https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators>
from .helpers import (  # pylint: disable=relative-beyond-top-level
    ic,
    thread_native_id_filter,
)
from .moduletools import moduleexport

# noinspection PyUnresolvedReferences
from .valuetyping import (
    Any,
    Coroutine,
    Literal,
    LiteralString,
    NamedTuple,
    ParamSpec,
    TypeIs,
    TypeVar,
    TypeVarTuple,
    Unpack,
    cast,
    reveal_type,
)

# https://docs.python.org/3.10/library/typing.html#typing.ParamSpec
InstanceObjectT = TypeVar("InstanceObjectT")
_FunCallResultT = TypeVar("_FunCallResultT")
_FunParamT = ParamSpec("_FunParamT")
# Maybe different if async or not
# https://stackoverflow.com/a/68746329/617339


# @overload
# def logdecorate(
#    func: Callable[_FunParamT, Awaitable[_FunCallResultT]]
# ) -> Callable[_FunParamT, Awaitable[_FunCallResultT]]: ...
#
#
# @overload
# def logdecorate(
#    func: Callable[_FunParamT, _FunCallResultT]
# ) -> Callable[_FunParamT, _FunCallResultT]: ...

# <https://stackoverflow.com/q/78206137>


# https://rednafi.com/python/typeguard_vs_typeis/
# https://peps.python.org/pep-0742/


def istypedcoroutinefunction(
    func: (
        Callable[_FunParamT, _FunCallResultT]
        | Callable[_FunParamT, Coroutine[Any, Any, _FunCallResultT]]
    ),
) -> TypeIs[Callable[_FunParamT, Coroutine[Any, Any, _FunCallResultT]]]:
    """Is the argument an awaitable function with given return type following PEP-0742?"""
    return iscoroutinefunction(func)


@moduleexport
def logdecorate(
    func: (
        Callable[_FunParamT, _FunCallResultT]
        | Callable[_FunParamT, Coroutine[Any, Any, _FunCallResultT]]
    ),
) -> (
    Callable[_FunParamT, _FunCallResultT]
    | Callable[_FunParamT, Coroutine[Any, Any, _FunCallResultT]]
):
    """Decorator to log start and stop into file 'decorated.log' with logging."""

    def setuplogger(funcname: str) -> logging.Logger:
        """ """
        thelogger: logging.Logger = logging.getLogger(f"logdecorate.{funcname}")
        the_format: str = "|".join(
            [
                "%(asctime)s",
                #            "%(name)s",#name of the logger
                #            "%(funcName)s",#not working, decorator
                func.__name__,
                #            "%(levelname)s",
                #            "%(processName)s (%(process)d)",
                "PID %(process)d",
                #            "%(threadName)s (%(thread_native)d)",
                "ThID %(thread_native)d",
                "%(message)s",
            ]
        )
        logformatter: logging.Formatter = logging.Formatter(the_format)
        logfilehandler: logging.FileHandler = logging.FileHandler("decorated.log")
        logfilehandler.setFormatter(logformatter)
        logfilehandler.addFilter(thread_native_id_filter)
        thelogger.addHandler(logfilehandler)
        if __debug__:
            thelogger.setLevel(logging.DEBUG)
        else:
            thelogger.setLevel(logging.INFO)
        return thelogger

    def logtiminglines(begintimings: os.times_result, endtimings: os.times_result) -> None:
        """ """
        title_line_format: LiteralString = "%11.11s|" * 5 + "%8.8s|"
        info_line_format: LiteralString = "%7.2f [s]|" * 5 + "%7.2f%%|"
        timingdiffs: tuple[float, ...] = tuple(b - a for (a, b) in zip(begintimings, endtimings))
        thelogger.info(
            title_line_format,
            "user",
            "system",
            "child_user",
            "child_system",
            "elapsed",
            "LOAD",
        )
        thelogger.info(
            info_line_format,
            *timingdiffs,
            100 * sum(timingdiffs[:4]) / timingdiffs[4] if timingdiffs[4] else 0,
        )

    # https://docs.python.org/3/library/logging.html#levels
    thelogger: logging.Logger = setuplogger(func.__name__)
    thelogger.debug("%s %s %s", type(func), dir(func), func.__annotations__)
    if istypedcoroutinefunction(func):
        # assert_type(func, Callable[_FunParamT, Awaitable[_FunCallResultT]])
        thelogger.debug("%s is a coro", reveal_type(func))

        #        thelogger.info("%s",type(func))
        #        thelogger.info("%s",dir(func))
        #        thelogger.info("%s",func.__annotations__)
        @wraps(wrapped=func)
        async def awrapped(*args: _FunParamT.args, **kwargs: _FunParamT.kwargs) -> _FunCallResultT:
            """ """
            # Pre-Execution
            thelogger.debug("LogDecorated ASYNC Start")
            begintimings: os.times_result = os.times()
            # Execution
            res: _FunCallResultT = await func(*args, **kwargs)
            # Post-Execution
            endtimings: os.times_result = os.times()
            logtiminglines(begintimings, endtimings)
            thelogger.debug(msg="LogDecorated ASYNC End")
            return res

        return awrapped
    # assert_type(func, Callable[_FunParamT, _FunCallResultT])
    thelogger.debug("%s is a synchronous function (no coro)", reveal_type(func))

    @wraps(wrapped=func)
    def wrapped(*args: _FunParamT.args, **kwargs: _FunParamT.kwargs) -> _FunCallResultT:
        """ """
        thelogger.debug("LogDecorated Start")
        begintimings: os.times_result = os.times()
        res: _FunCallResultT = func(*args, **kwargs)
        endtimings: os.times_result = os.times()
        logtiminglines(begintimings, endtimings)
        thelogger.debug("LogDecorated End")
        return res

    return wrapped


# Good info for timing measurement <https://stackoverflow.com/a/62115793>


@moduleexport
def timing_wall(
    func: Callable[_FunParamT, _FunCallResultT],
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measure WALL-Clock monotonic."""

    @wraps(func)
    def wrapped(
        *args: _FunParamT.args,
        **kwargs: _FunParamT.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: float | Literal[0] = time.monotonic()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float | Literal[0] = time.monotonic()
        if before and after:
            print(func.__name__, float(after) - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


@moduleexport
def portable_timing(
    func: (
        Callable[_FunParamT, _FunCallResultT]
        | Callable[_FunParamT, Coroutine[Any, Any, _FunCallResultT]]
    ),
) -> (
    Callable[_FunParamT, _FunCallResultT]
    | Callable[_FunParamT, Coroutine[Any, Any, _FunCallResultT]]
):
    """Like LINUX-TIME Command."""
    if istypedcoroutinefunction(func):

        @wraps(func)
        async def awrapped(
            *args: _FunParamT.args,
            **kwargs: _FunParamT.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: tuple[int, os.times_result] = (time.perf_counter_ns(), os.times())
            retval: _FunCallResultT = await func(*args, **kwargs)
            after: tuple[int, os.times_result] = (time.perf_counter_ns(), os.times())
            if before and after:
                wall_diff: float = (after[0] - before[0]) / 1e9
                user_diff: float = (
                    after[1].user
                    - before[1].user
                    + after[1].children_user
                    - before[1].children_user
                )
                system_diff: float = (
                    after[1].system
                    - before[1].system
                    + after[1].children_system
                    - before[1].children_system
                )
                print(f"{func.__name__:10} {args} {kwargs}")
                print(
                    f"{wall_diff:8.3f} [s]",
                    f"\t(User: {user_diff:8.3f} [s]," f"\tSystem: {system_diff:8.3f} [s])",
                    f"{100 * (user_diff + system_diff) / wall_diff:6.2f}% Load",
                )
            return retval

        return awrapped

    @wraps(func)
    def wrapped(
        *args: _FunParamT.args,
        **kwargs: _FunParamT.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: tuple[int, os.times_result] = (time.perf_counter_ns(), os.times())
        retval: _FunCallResultT = func(*args, **kwargs)
        after: tuple[int, os.times_result] = (time.perf_counter_ns(), os.times())
        if before and after:
            wall_diff = (after[0] - before[0]) / 1e9
            user_diff = (
                after[1].user - before[1].user + after[1].children_user - before[1].children_user
            )
            system_diff = (
                after[1].system
                - before[1].system
                + after[1].children_system
                - before[1].children_system
            )
            print(f"{func.__name__:10} {args} {kwargs}")
            print(
                f"{wall_diff:8.3f} [s]",
                f"\t(User: {user_diff:8.3f} [s]," f"\tSystem {system_diff:8.3f} [s])",
                f"{100 * (user_diff + system_diff) / wall_diff:6.2f}% Load",
            )
        return retval

    return wrapped


@moduleexport
def linuxtime(
    func: Callable[_FunParamT, _FunCallResultT],
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measure like unix/linux time command."""

    @wraps(func)
    def wrapped(
        *args: _FunParamT.args,
        **kwargs: _FunParamT.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: os.times_result = os.times()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: os.times_result = os.times()
        if before and after:
            print("time function\t", func.__name__)
            wall_time: float = after.elapsed - before.elapsed
            user_time: float = (
                after.user - before.user + after.children_user - before.children_user
            )
            sys_time: float = (
                after.system - before.system + after.children_system - before.children_system
            )
            print(
                "user: ",
                after.user - before.user,
                "+",
                after.children_user - before.children_user,
                "=",
                user_time,
                "[s]",
            )
            print(
                "system",
                after.system - before.system,
                "+",
                after.children_system - before.children_system,
                "=",
                sys_time,
                "[s]",
            )
            print(f"real: {wall_time:.3} [s]\t {(user_time + sys_time) / wall_time} % load")
        return retval

    return wrapped


if os.name == "posix":
    import resource  # pylint:disable=import-error

    @moduleexport
    def linuxtime_resource(
        func: Callable[_FunParamT, _FunCallResultT],
    ) -> Callable[_FunParamT, _FunCallResultT]:
        """Measure like unix/linux time command."""

        @wraps(func)
        def wrapped(
            *args: _FunParamT.args,
            **kwargs: _FunParamT.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: float | Literal[0] = time.monotonic()
            childbefore: resource.struct_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
            selfbefore: resource.struct_rusage = resource.getrusage(resource.RUSAGE_SELF)
            retval: _FunCallResultT = func(*args, **kwargs)
            selfafter: resource.struct_rusage = resource.getrusage(resource.RUSAGE_SELF)
            childafter: resource.struct_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
            after: float | Literal[0] = time.monotonic()
            if all((childbefore, selfbefore, selfafter, childafter, before, after)):
                print("time function\t", func.__name__)
                wall_time: float = after - before
                user_time: float = (
                    selfafter.ru_utime
                    - selfbefore.ru_utime
                    + childafter.ru_utime
                    - childbefore.ru_utime
                )
                sys_time: float = (
                    selfafter.ru_stime
                    - selfbefore.ru_stime
                    + childafter.ru_stime
                    - childbefore.ru_stime
                )
                print(
                    "user: ",
                    selfafter.ru_utime - selfbefore.ru_utime,
                    "+",
                    childafter.ru_utime - childbefore.ru_utime,
                    "=",
                    user_time,
                    "[s]",
                )
                print(
                    "system",
                    selfafter.ru_stime - selfbefore.ru_stime,
                    "+",
                    childafter.ru_stime - childbefore.ru_stime,
                    "=",
                    sys_time,
                    "[s]",
                )
                print(f"real: {wall_time:.3} [s]\t {(user_time + sys_time) / wall_time} % load")
            return retval

        return wrapped

    @moduleexport
    def timing_resource(
        func: Callable[_FunParamT, _FunCallResultT],
    ) -> Callable[_FunParamT, _FunCallResultT]:
        """Measure execution times by resource."""

        @wraps(func)
        def wrapped(
            *args: _FunParamT.args,
            **kwargs: _FunParamT.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: float | Literal[0] = sum(resource.getrusage(resource.RUSAGE_SELF)[:2])
            retval: _FunCallResultT = func(*args, **kwargs)
            after: float | Literal[0] = sum(resource.getrusage(resource.RUSAGE_SELF)[:2])
            if before and after:
                print(func.__name__, float(after) - before)
            return retval

        return wrapped


try:
    # noinspection PyUnresolvedReferences
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    @moduleexport
    def timing_psutil(
        func: Callable[_FunParamT, _FunCallResultT],
    ) -> Callable[_FunParamT, _FunCallResultT]:
        """Measures execution times by psutil."""

        @wraps(func)
        def wrapped(
            *args: _FunParamT.args,
            **kwargs: _FunParamT.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: NamedTuple = psutil.Process().cpu_times()
            retval: _FunCallResultT = func(*args, **kwargs)
            after: NamedTuple = psutil.Process().cpu_times()
            delta: list[float] = [end - start for start, end in zip(before, after)]
            print(func.__name__, delta, sum(delta))
            return retval

        return wrapped  # cast(FunctionTypeVar, wrapped)


@moduleexport
def timing_thread_time(
    func: Callable[_FunParamT, _FunCallResultT],
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measures execution times by time (thread)."""

    @wraps(func)
    def wrapped(
        *args: _FunParamT.args,
        **kwargs: _FunParamT.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: float = time.thread_time()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float = time.thread_time()
        print(func.__name__, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


@moduleexport
def timing_process_time(
    func: Callable[_FunParamT, _FunCallResultT],
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measures execution times by time (process)."""

    @wraps(func)
    def wrapped(*args: _FunParamT.args, **kwargs: _FunParamT.kwargs) -> _FunCallResultT:
        """Run with timing."""
        before: float = time.process_time()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float = time.process_time()
        print(func.__name__, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


@moduleexport
class LazyProperty(property):
    """
    Decorator for properties, which will be only evaluated if needed.

    implementation based on ideas given in
    <https://stevenloria.com/lazy-properties>
    """

    # <https://towardsdatascience.com/2807ef52d273>
    # = <https://archive.is/GfSvY>
    # archived under <https://archive.is/8yiRH> and
    # <https://web.archive.org/web/20210514102257/https://stevenloria.com/lazy-properties/>
    # having a look at <https://www.programiz.com/python-programming/property>
    # might also help. Further interesting is
    # <https://stackoverflow.com/questions/7151890#answer-7152065>
    def __init__(
        self: LazyProperty,
        getterfunction: Callable[
            [InstanceObjectT],  # pyright: ignore[reportInvalidTypeVarUse]
            _FunCallResultT,  # pyright: ignore[reportInvalidTypeVarUse]
        ],
    ) -> None:
        """Initialize special attribute and rest from super."""
        attr_name: str = f"_lazy_{getterfunction.__name__}"

        def _lazy_getterfunction(instanceobj: InstanceObjectT) -> _FunCallResultT:
            """Check if value present, if not calculate."""
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return cast(_FunCallResultT, getattr(instanceobj, attr_name))

        super().__init__(_lazy_getterfunction)


ParameterTupleT = TypeVarTuple("ParameterTupleT")


@moduleexport
def memoize(
    func: Callable[[Unpack[ParameterTupleT]], _FunCallResultT],
) -> Callable[[Unpack[ParameterTupleT]], _FunCallResultT]:
    """decorater for caching calls
    thanks to
    <https://towardsdatascience.com/python-decorators-for-data-science-6913f717669a#879f>
    <https://towardsdatascience.com/12-python-decorators-to-take-your-code-to-the-next-level-a910a1ab3e99>
    """
    cache: dict[tuple[Unpack[ParameterTupleT]], _FunCallResultT] = {}

    @wraps(func)
    def wrapper(*args: Unpack[ParameterTupleT]) -> _FunCallResultT:
        """ """
        if args in cache:
            return cache[args]
        result: _FunCallResultT = func(*args)
        cache[args] = result
        return result

    return wrapper
