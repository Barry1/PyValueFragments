"""module holding decorators."""

from __future__ import annotations

import logging
import os
import time
from functools import wraps

# no longer use that from asyncio as deprecated from 3.14
from inspect import iscoroutinefunction
from types import FunctionType  # , CoroutineType

# typing with the help of
# <https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators>
from .helpers import (  # pylint: disable=relative-beyond-top-level
    ic,
    print_time_result,
    thread_native_id_filter,
)
from .moduletools import moduleexport

# noinspection PyUnresolvedReferences
from .valuetyping import (  # Coroutine,; TypeGuard,
    Any,
    Callable,
    Coroutine,
    Literal,
    NamedTuple,
    TypeIs,
    assert_type,
    cast,
    reveal_type,
)

# from types import CoroutineType
# https://docs.python.org/3/reference/compound_stmts.html#type-params
# This shows, how to use type params in functions and classes.


# https://docs.python.org/3.10/library/typing.html#typing.ParamSpec
# Maybe different if async or not
# https://stackoverflow.com/a/68746329/617339


# @overload
# def logdecorate(
#    func: Callable[_fun_param_T, Awaitable[_FunCallResultT]]
# ) -> Callable[_FunParamP, Awaitable[_FunCallResultT]]: ...
#
#
# @overload
# def logdecorate(
#    func: Callable[_FunParamP, _FunCallResultT]
# ) -> Callable[_FunParamP, _FunCallResultT]: ...

# <https://stackoverflow.com/q/78206137>


def istypedcoroutinefunction[T, **ParamP](
    func: Callable[ParamP, Coroutine[Any, Any, T]] | Callable[ParamP, T],
) -> TypeIs[Callable[ParamP, Coroutine[Any, Any, T]]]:
    """Is the argument an awaitable function?"""
    # with given return type following PEP-0742?"""
    # https://rednafi.com/python/typeguard_vs_typeis/
    # https://peps.python.org/pep-0742/
    return iscoroutinefunction(func)


def is_coroutine_function[T, **ParamP](
    func: Callable[ParamP, T] | Callable[ParamP, Coroutine[Any, Any, T]],
) -> TypeIs[Callable[ParamP, Coroutine[Any, Any, T]]]:
    """Is the argument an awaitable function?"""
    # with given return type following PEP-0742?"""
    return (
        isinstance(func, FunctionType)
        and hasattr(func, "__code__")
        and func.__code__.co_flags & 0x80 != 0
    )


@moduleexport
def logdecorate[T, **ParamP](
    func: Callable[ParamP, T] | Callable[ParamP, Coroutine[Any, Any, T]],
) -> Callable[ParamP, Coroutine[Any, Any, T]] | Callable[ParamP, T]:
    """Decorator: Log start and stop into 'decorated.log'"""

    def setuplogger(funcname: str) -> logging.Logger:
        """Set up a new Logger for my needs"""
        thenewlogger: logging.Logger = logging.getLogger(
            f"logdecorate.{funcname}"
        )
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
        logfilehandler: logging.FileHandler = logging.FileHandler(
            "decorated.log"
        )
        logfilehandler.setFormatter(logformatter)
        logfilehandler.addFilter(thread_native_id_filter)
        thenewlogger.addHandler(logfilehandler)
        thenewlogger.setLevel(logging.DEBUG if __debug__ else logging.INFO)
        return thenewlogger

    def logtiminglines(
        begintimings: os.times_result,
        endtimings: os.times_result,
        theloggertouse: logging.Logger,
    ) -> None:
        """log details from timings"""
        title_line_format: str = "%11.11s|" * 5 + "%8.8s|"
        info_line_format: str = "%7.2f [s]|" * 5 + "%7.2f%%|"
        timingdiffs: tuple[float, ...] = tuple(
            b - a for (a, b) in zip(begintimings, endtimings)
        )
        theloggertouse.info(
            title_line_format,
            "user",
            "system",
            "child_user",
            "child_system",
            "elapsed",
            "LOAD",
        )
        theloggertouse.info(
            info_line_format,
            *timingdiffs,
            (
                100 * sum(timingdiffs[:4]) / timingdiffs[4]
                if timingdiffs[4]
                else 0
            ),
        )

    # https://docs.python.org/3/library/logging.html#levels
    thelogger: logging.Logger = setuplogger(func.__name__)
    thelogger.debug("%s %s %s", type(func), dir(func), func.__annotations__)
    if istypedcoroutinefunction(func=func):
        #    if is_coroutine_function(func=func):
        assert_type(func, Callable[ParamP, Coroutine[Any, Any, T]])
        # assert isinstance(func, Callable[ParamP, Coroutine[Any, Any, T]])
        thelogger.debug("%s is a coro: %s", func, reveal_type(func))
        #        thelogger.info("%s",type(func))
        #        thelogger.info("%s",dir(func))
        #        thelogger.info("%s",func.__annotations__)
        # @wraps(wrapped=func)

        async def awrapped(*args: ParamP.args, **kwargs: ParamP.kwargs) -> T:
            """Wrapped function for the async case."""
            # Pre-Execution
            thelogger.debug(msg="LogDecorated ASYNC Start")
            begintimings: os.times_result = os.times()
            # Execution
            res: T = await func(*args, **kwargs)
            # Post-Execution
            endtimings: os.times_result = os.times()
            logtiminglines(
                begintimings=begintimings,
                endtimings=endtimings,
                theloggertouse=thelogger,
            )
            thelogger.debug(msg="LogDecorated ASYNC End")
            return res

        return awrapped
    assert_type(func, Callable[ParamP, T])
    # assert isinstance(func, Callable[ParamP, T])
    thelogger.debug(
        "%s is a synchronous function (no coro): %s", func, reveal_type(func)
    )

    # @wraps(wrapped=func)
    def wrapped(*args: ParamP.args, **kwargs: ParamP.kwargs) -> T:
        """ """
        thelogger.debug(msg="LogDecorated Start")
        begintimings: os.times_result = os.times()
        res: T = func(*args, **kwargs)
        endtimings: os.times_result = os.times()
        logtiminglines(
            begintimings=begintimings,
            endtimings=endtimings,
            theloggertouse=thelogger,
        )
        thelogger.debug(msg="LogDecorated End")
        return res

    return wrapped


# Good info for timing measurement <https://stackoverflow.com/a/62115793>


@moduleexport
def timing_wall[**_FunParamP, _FunCallResultT](
    func: Callable[_FunParamP, _FunCallResultT],
) -> Callable[_FunParamP, _FunCallResultT]:
    """Measure WALL-Clock monotonic."""

    @wraps(func)
    def wrapped(
        *args: _FunParamP.args,
        **kwargs: _FunParamP.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: float | Literal[0] = time.monotonic()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float | Literal[0] = time.monotonic()
        if before and after:
            print(func.__name__, float(after) - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


def calcdiffs(
    before: tuple[int, os.times_result], after: tuple[int, os.times_result]
) -> tuple[float, float, float]:
    """Evaluate Timing-Diffs."""
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
    return wall_diff, user_diff, system_diff


@moduleexport
def portable_timing[**_FunParamP, _FunCallResultT](
    func: (
        Callable[_FunParamP, _FunCallResultT]
        | Callable[_FunParamP, Coroutine[Any, Any, _FunCallResultT]]
    ),
) -> (
    Callable[_FunParamP, _FunCallResultT]
    | Callable[_FunParamP, Coroutine[Any, Any, _FunCallResultT]]
):
    """Like LINUX-TIME Command."""
    if istypedcoroutinefunction(func):

        @wraps(func)
        async def awrapped(
            *args: _FunParamP.args,
            **kwargs: _FunParamP.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: tuple[int, os.times_result] = (
                time.perf_counter_ns(),
                os.times(),
            )
            retval: _FunCallResultT = await func(*args, **kwargs)
            after: tuple[int, os.times_result] = (
                time.perf_counter_ns(),
                os.times(),
            )
            if before and after:
                wall_diff, user_diff, system_diff = calcdiffs(before, after)
                print(f"{func.__name__:10} {args} {kwargs}")
                print_time_result(wall_diff, user_diff, system_diff)
            return retval

        return awrapped

    @wraps(func)
    def wrapped(
        *args: _FunParamP.args,
        **kwargs: _FunParamP.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: tuple[int, os.times_result] = (
            time.perf_counter_ns(),
            os.times(),
        )
        retval: _FunCallResultT = func(*args, **kwargs)
        after: tuple[int, os.times_result] = (
            time.perf_counter_ns(),
            os.times(),
        )
        if before and after:
            wall_diff, user_diff, system_diff = calcdiffs(before, after)
            print(f"{func.__name__:10} {args} {kwargs}")
            print_time_result(wall_diff, user_diff, system_diff)
        return retval

    return wrapped


@moduleexport
def linuxtime[**_FunParamP, _FunCallResultT](
    func: Callable[_FunParamP, _FunCallResultT],
) -> Callable[_FunParamP, _FunCallResultT]:
    """Measure like unix/linux time command."""

    @wraps(func)
    def wrapped(
        *args: _FunParamP.args,
        **kwargs: _FunParamP.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: os.times_result = os.times()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: os.times_result = os.times()
        if before and after:
            print("time function\t", func.__name__)
            print_time_result(
                wall=after.elapsed - before.elapsed,
                user=after.user
                - before.user
                + after.children_user
                - before.children_user,
                system=after.system
                - before.system
                + after.children_system
                - before.children_system,
            )
        return retval

    return wrapped


if os.name == "posix":
    import resource  # pylint:disable=import-error

    @moduleexport
    def linuxtime_resource[**_FunParamP, _FunCallResultT](
        func: Callable[_FunParamP, _FunCallResultT],
    ) -> Callable[_FunParamP, _FunCallResultT]:
        """Measure like unix/linux time command."""

        @wraps(func)
        def wrapped(
            *args: _FunParamP.args,
            **kwargs: _FunParamP.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: float | Literal[0] = time.monotonic()
            childbefore: resource.struct_rusage = resource.getrusage(
                resource.RUSAGE_CHILDREN
            )
            selfbefore: resource.struct_rusage = resource.getrusage(
                resource.RUSAGE_SELF
            )
            retval: _FunCallResultT = func(*args, **kwargs)
            selfafter: resource.struct_rusage = resource.getrusage(
                resource.RUSAGE_SELF
            )
            childafter: resource.struct_rusage = resource.getrusage(
                resource.RUSAGE_CHILDREN
            )
            after: float | Literal[0] = time.monotonic()
            if all(
                (childbefore, selfbefore, selfafter, childafter, before, after)
            ):
                print("time function\t", func.__name__)
                print_time_result(
                    wall=after - before,
                    user=selfafter.ru_utime
                    - selfbefore.ru_utime
                    + childafter.ru_utime
                    - childbefore.ru_utime,
                    system=selfafter.ru_stime
                    - selfbefore.ru_stime
                    + childafter.ru_stime
                    - childbefore.ru_stime,
                )
            return retval

        return wrapped

    @moduleexport
    def timing_resource[**_FunParamP, _FunCallResultT](
        func: Callable[_FunParamP, _FunCallResultT],
    ) -> Callable[_FunParamP, _FunCallResultT]:
        """Measure execution times by resource."""

        @wraps(func)
        def wrapped(
            *args: _FunParamP.args,
            **kwargs: _FunParamP.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: float | Literal[0] = sum(
                resource.getrusage(resource.RUSAGE_SELF)[:2]
            )
            retval: _FunCallResultT = func(*args, **kwargs)
            after: float | Literal[0] = sum(
                resource.getrusage(resource.RUSAGE_SELF)[:2]
            )
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
    def timing_psutil[**_FunParamP, _FunCallResultT](
        func: Callable[_FunParamP, _FunCallResultT],
    ) -> Callable[_FunParamP, _FunCallResultT]:
        """Measures execution times by psutil."""

        @wraps(func)
        def wrapped(
            *args: _FunParamP.args,
            **kwargs: _FunParamP.kwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: NamedTuple = psutil.Process().cpu_times()
            retval: _FunCallResultT = func(*args, **kwargs)
            after: NamedTuple = psutil.Process().cpu_times()
            delta: list[float] = [
                end - start for start, end in zip(before, after)
            ]
            print(func.__name__, delta, sum(delta))
            return retval

        return wrapped  # cast(FunctionTypeVar, wrapped)


@moduleexport
def timing_thread_time[**_FunParamP, _FunCallResultT](
    func: Callable[_FunParamP, _FunCallResultT],
) -> Callable[_FunParamP, _FunCallResultT]:
    """Measures execution times by time (thread)."""

    @wraps(func)
    def wrapped(
        *args: _FunParamP.args,
        **kwargs: _FunParamP.kwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: float = time.thread_time()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float = time.thread_time()
        print(func.__name__, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


@moduleexport
def timing_process_time[**_FunParamP, _FunCallResultT](
    func: Callable[_FunParamP, _FunCallResultT],
) -> Callable[_FunParamP, _FunCallResultT]:
    """Measures execution times by time (process)."""

    @wraps(func)
    def wrapped(
        *args: _FunParamP.args, **kwargs: _FunParamP.kwargs
    ) -> _FunCallResultT:
        """Run with timing."""
        before: float = time.process_time()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float = time.process_time()
        print(func.__name__, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


@moduleexport
class LazyProperty[InstanceObjectT, _FunCallResultT](property):
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
        self,  #: LazyProperty
        getterfunction: Callable[[InstanceObjectT], _FunCallResultT],
    ) -> None:
        """Initialize special attribute and rest from super."""
        attr_name: str = f"_lazy_{getterfunction.__name__}"

        def _lazy_getterfunction(
            instanceobj: InstanceObjectT,
        ) -> _FunCallResultT:
            """Check if value present, if not calculate."""
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return cast(_FunCallResultT, getattr(instanceobj, attr_name))

        super().__init__(_lazy_getterfunction)


@moduleexport
def memoize[*_ParamTupleTs, _FunCallResultT](
    func: Callable[[*_ParamTupleTs], _FunCallResultT],
) -> Callable[[*_ParamTupleTs], _FunCallResultT]:
    """decorater for caching calls
    thanks to
    <https://towardsdatascience.com/python-decorators-for-data-science-6913f717669a#879f>
    <https://towardsdatascience.com/12-python-decorators-to-take-your-code-to-the-next-level-a910a1ab3e99>
    """
    cache: dict[tuple[*_ParamTupleTs], _FunCallResultT] = {}

    # @wraps(func)
    def wrapper(*args: *_ParamTupleTs) -> _FunCallResultT:
        """ """
        if args in cache:
            return cache[args]
        result: _FunCallResultT = func(*args)
        cache[args] = result
        return result

    return wrapper
