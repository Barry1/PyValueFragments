"""module holding decorators."""
from __future__ import annotations

import logging
import os
import sys
import time
from functools import wraps

# typing with the help of
# <https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators>
from typing import Callable, Literal, LiteralString, NamedTuple, TypeVar, cast

from typing_extensions import TypeVarTuple, Unpack

# from typing_extensions import Self
from .helpers import (  # pylint: disable=relative-beyond-top-level
    ic,
    thread_native_id_filter,
)

# https://docs.python.org/3.10/library/typing.html#typing.ParamSpec
if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec, ParamSpecArgs, ParamSpecKwargs
else:
    from typing import (  # pylint: disable=no-name-in-module
        ParamSpec,
        ParamSpecArgs,
        ParamSpecKwargs,
    )
InstanceObjectT = TypeVar("InstanceObjectT")
_FunCallResultT = TypeVar("_FunCallResultT")
_FunParamT = ParamSpec("_FunParamT")
__all__: list[str] = []


def logdecorate(
    func: Callable[_FunParamT, _FunCallResultT]
) -> Callable[_FunParamT, _FunCallResultT]:
    """Decorator to log start and stop into file 'decorated.log' with logging."""
    thelogger: logging.Logger = logging.getLogger("logdecorate")
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
    # https://docs.python.org/3/library/logging.html#levels
    if __debug__:
        thelogger.setLevel(logging.DEBUG)
    else:
        thelogger.setLevel(logging.INFO)

    @wraps(func)
    def wrapped(*args: _FunParamT.args, **kwargs: _FunParamT.kwargs) -> _FunCallResultT:
        thelogger.debug("LogDecorated Start")
        begintimings: os.times_result = os.times()
        res: _FunCallResultT = func(*args, **kwargs)
        endtimings: os.times_result = os.times()
        title_line_format: LiteralString = "%11.11s|" * 5 + "%8.8s|"
        info_line_format: LiteralString = "%7.2f [s]|" * begintimings.n_fields + "%7.2f%%|"
        thelogger.info(
            title_line_format, "user", "system", "child_user", "child_system", "elapsed", "LOAD"
        )
        thelogger.info(
            info_line_format,
            *tuple(b - a for (a, b) in zip(begintimings, endtimings)),
            100
            * (sum(endtimings[:4]) - sum(begintimings[:4]))
            / (endtimings.elapsed - begintimings.elapsed),
        )
        thelogger.debug("LogDecorated End")
        return res

    return wrapped


__all__.append("logdecorate")

# Good info for timing measurement <https://stackoverflow.com/a/62115793>


def timing_wall(
    func: Callable[_FunParamT, _FunCallResultT]
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measure WALL-Clock monotonic."""

    @wraps(func)
    def wrapped(
        *args: ParamSpecArgs,
        **kwargs: ParamSpecKwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: float | Literal[0] = time.monotonic()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float | Literal[0] = time.monotonic()
        if before and after:
            print(func.__name__, float(after) - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


__all__.append("timing_wall")


def linuxtime(
    func: Callable[_FunParamT, _FunCallResultT]
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measure like unix/linux time command."""

    @wraps(func)
    def wrapped(
        *args: ParamSpecArgs,
        **kwargs: ParamSpecKwargs,
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


__all__.append("linuxtime")


try:
    # noinspection PyUnresolvedReferences
    import resource
except ImportError:
    ic("resource is not available")
else:

    def linuxtime_resource(
        func: Callable[_FunParamT, _FunCallResultT]
    ) -> Callable[_FunParamT, _FunCallResultT]:
        """Measure like unix/linux time command."""

        @wraps(func)
        def wrapped(
            *args: ParamSpecArgs,
            **kwargs: ParamSpecKwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: float | Literal[0] = time.monotonic()
            childbefore: resource.struct_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
            selfbefore: resource.struct_rusage = resource.getrusage(resource.RUSAGE_SELF)
            retval: _FunCallResultT = func(*args, **kwargs)
            selfafter: resource.struct_rusage = resource.getrusage(resource.RUSAGE_SELF)
            childafter: resource.struct_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
            after: float | Literal[0] = time.monotonic()
            if childbefore and selfbefore and selfafter and childafter and before and after:
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

    __all__.append("linuxtime_resource")

    def timing_resource(
        func: Callable[_FunParamT, _FunCallResultT]
    ) -> Callable[_FunParamT, _FunCallResultT]:
        """Measure execution times by resource."""

        @wraps(func)
        def wrapped(
            *args: ParamSpecArgs,
            **kwargs: ParamSpecKwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: float | Literal[0] = sum(resource.getrusage(resource.RUSAGE_SELF)[:2])
            retval: _FunCallResultT = func(*args, **kwargs)
            after: float | Literal[0] = sum(resource.getrusage(resource.RUSAGE_SELF)[:2])
            if before and after:
                print(func.__name__, float(after) - before)
            return retval

        return wrapped  # cast(FunctionTypeVar, wrapped)

    __all__.append("timing_resource")


try:
    # noinspection PyUnresolvedReferences
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    def timing_psutil(
        func: Callable[_FunParamT, _FunCallResultT]
    ) -> Callable[_FunParamT, _FunCallResultT]:
        """Measures execution times by psutil."""

        @wraps(func)
        def wrapped(
            *args: ParamSpecArgs,
            **kwargs: ParamSpecKwargs,
        ) -> _FunCallResultT:
            """Run with timing."""
            before: NamedTuple = psutil.Process().cpu_times()
            retval: _FunCallResultT = func(*args, **kwargs)
            after: NamedTuple = psutil.Process().cpu_times()
            delta: list[float] = [end - start for start, end in zip(before, after)]
            print(func.__name__, delta, sum(delta))
            return retval

        return wrapped  # cast(FunctionTypeVar, wrapped)

    __all__.append("timing_psutil")


def timing_thread_time(
    func: Callable[_FunParamT, _FunCallResultT]
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measures execution times by time (thread)."""

    @wraps(func)
    def wrapped(
        *args: ParamSpecArgs,
        **kwargs: ParamSpecKwargs,
    ) -> _FunCallResultT:
        """Run with timing."""
        before: float = time.thread_time()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float = time.thread_time()
        print(func.__name__, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


__all__.append("timing_thread_time")


def timing_process_time(
    func: Callable[_FunParamT, _FunCallResultT]
) -> Callable[_FunParamT, _FunCallResultT]:
    """Measures execution times by time (process)."""

    @wraps(func)
    def wrapped(*args: ParamSpecArgs, **kwargs: ParamSpecKwargs) -> _FunCallResultT:
        """Run with timing."""
        before: float = time.process_time()
        retval: _FunCallResultT = func(*args, **kwargs)
        after: float = time.process_time()
        print(func.__name__, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


__all__.append("timing_process_time")


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


__all__.append("LazyProperty")

ParameterTupleT = TypeVarTuple("ParameterTupleT")


def memoize(
    func: Callable[[Unpack[ParameterTupleT]], _FunCallResultT]
) -> Callable[[Unpack[ParameterTupleT]], _FunCallResultT]:
    """decorater for caching calls
    thanks to
    <https://towardsdatascience.com/python-decorators-for-data-science-6913f717669a#879f>
    <https://towardsdatascience.com/12-python-decorators-to-take-your-code-to-the-next-level-a910a1ab3e99>
    """
    cache: dict[tuple[Unpack[ParameterTupleT]], _FunCallResultT] = {}

    @wraps(func)
    def wrapper(*args: Unpack[ParameterTupleT]) -> _FunCallResultT:
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


__all__.append("memoize")
