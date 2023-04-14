"""module holding decorators."""
from __future__ import annotations

import sys
import time
from functools import wraps

# typing with the help of
# <https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators>
from typing import Callable, Literal, NamedTuple, TypeVar, cast

from typing_extensions import TypeVarTuple, Unpack

# from typing_extensions import Self
from .helpers import ic  # pylint: disable=relative-beyond-top-level

# https://docs.python.org/3.10/library/typing.html#typing.ParamSpec
if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec, ParamSpecArgs, ParamSpecKwargs
else:
    from typing import (  # pylint: disable=no-name-in-module
        ParamSpec,
        ParamSpecArgs,
        ParamSpecKwargs,
    )
ParamType = ParamSpec("ParamType")
ResultT = TypeVar("ResultT")
InstanceObjectT = TypeVar("InstanceObjectT")
__all__: list[str] = []
# Good info for timing measurement <https://stackoverflow.com/a/62115793>


def timing_wall(func: Callable[ParamType, ResultT]) -> Callable[ParamType, ResultT]:
    """Measure WALL-Clock monotonic."""

    @wraps(func)
    def wrapped(
        *args: ParamSpecArgs,
        **kwargs: ParamSpecKwargs,
    ) -> ResultT:
        """Run with timing."""
        before: float | Literal[0] = time.monotonic()
        retval: ResultT = func(*args, **kwargs)
        after: float | Literal[0] = time.monotonic()
        if before and after:
            print(func.__name__, float(after) - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


__all__.append("timing_wall")


def linuxtime(func: Callable[ParamType, ResultT]) -> Callable[ParamType, ResultT]:
    """Measure like unix/linux time command."""

    @wraps(func)
    def wrapped(
        *args: ParamSpecArgs,
        **kwargs: ParamSpecKwargs,
    ) -> ResultT:
        """Run with timing."""
        before: os.times_result = os.times()
        retval: ResultT = func(*args, **kwargs)
        after: os.times_result = os.times()
        if before and after:
            print("time function\t", func.__name__)
            WALLtime: float = after.elapsed - before.elapsed
            USERtime: float = after.user - before.user + after.children_user - before.children_user
            SYStime: float = (
                after.system - before.system + after.children_system - before.children_system
            )
            print(
                "user: ",
                after.user - before.user,
                "+",
                after.children_user - before.children_user,
                "=",
                USERtime,
                "[s]",
            )
            print(
                "system",
                after.system - before.system,
                "+",
                after.children_system - before.children_system,
                "=",
                SYStime,
                "[s]",
            )
            print("real: ", WALLtime, "[s] beeing", (USERtime + SYStime) / WALLtime, "% load")
        return retval

    return wrapped


__all__.append("linuxtime")


try:
    # noinspection PyUnresolvedReferences
    import resource
except ImportError:
    ic("resource is not available")
else:

    def linuxtime_resource(func: Callable[ParamType, ResultT]) -> Callable[ParamType, ResultT]:
        """Measure like unix/linux time command."""

        @wraps(func)
        def wrapped(
            *args: ParamSpecArgs,
            **kwargs: ParamSpecKwargs,
        ) -> ResultT:
            """Run with timing."""
            before: float | Literal[0] = time.monotonic()
            childbefore: resource.struct_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
            selfbefore: resource.struct_rusage = resource.getrusage(resource.RUSAGE_SELF)
            retval: ResultT = func(*args, **kwargs)
            selfafter: resource.struct_rusage = resource.getrusage(resource.RUSAGE_SELF)
            childafter: resource.struct_rusage = resource.getrusage(resource.RUSAGE_CHILDREN)
            after: float | Literal[0] = time.monotonic()
            if childbefore and selfbefore and selfafter and childafter and before and after:
                print("time function\t", func.__name__)
                WALLtime: float = after - before
                USERtime: float = (
                    selfafter.ru_utime
                    - selfbefore.ru_utime
                    + childafter.ru_utime
                    - childbefore.ru_utime
                )
                SYStime: float = (
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
                    USERtime,
                    "[s]",
                )
                print(
                    "system",
                    selfafter.ru_stime - selfbefore.ru_stime,
                    "+",
                    childafter.ru_stime - childbefore.ru_stime,
                    "=",
                    SYStime,
                    "[s]",
                )
                print("real: ", WALLtime, "[s] beeing", (USERtime + SYStime) / WALLtime, "% load")
            return retval

        return wrapped

    __all__.append("linuxtime_resource")

    def timing_resource(func: Callable[ParamType, ResultT]) -> Callable[ParamType, ResultT]:
        """Measure execution times by resource."""

        @wraps(func)
        def wrapped(
            *args: ParamSpecArgs,
            **kwargs: ParamSpecKwargs,
        ) -> ResultT:
            """Run with timing."""
            before: float | Literal[0] = sum(resource.getrusage(resource.RUSAGE_SELF)[:2])
            retval: ResultT = func(*args, **kwargs)
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

    def timing_psutil(func: Callable[ParamType, ResultT]) -> Callable[ParamType, ResultT]:
        """Measures execution times by psutil."""

        @wraps(func)
        def wrapped(
            *args: ParamSpecArgs,
            **kwargs: ParamSpecKwargs,
        ) -> ResultT:
            """Run with timing."""
            before: NamedTuple = psutil.Process().cpu_times()
            retval: ResultT = func(*args, **kwargs)
            after: NamedTuple = psutil.Process().cpu_times()
            delta: list[float] = [end - start for start, end in zip(before, after)]
            print(func.__name__, delta, sum(delta))
            return retval

        return wrapped  # cast(FunctionTypeVar, wrapped)

    __all__.append("timing_psutil")


def timing_thread_time(func: Callable[ParamType, ResultT]) -> Callable[ParamType, ResultT]:
    """Measures execution times by time (thread)."""

    @wraps(func)
    def wrapped(
        *args: ParamSpecArgs,
        **kwargs: ParamSpecKwargs,
    ) -> ResultT:
        """Run with timing."""
        before: float = time.thread_time()
        retval: ResultT = func(*args, **kwargs)
        after: float = time.thread_time()
        print(func.__name__, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


__all__.append("timing_thread_time")


def timing_process_time(func: Callable[ParamType, ResultT]) -> Callable[ParamType, ResultT]:
    """Measures execution times by time (process)."""

    @wraps(func)
    def wrapped(*args: ParamSpecArgs, **kwargs: ParamSpecKwargs) -> ResultT:
        """Run with timing."""
        before: float = time.process_time()
        retval: ResultT = func(*args, **kwargs)
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
            ResultT,  # pyright: ignore[reportInvalidTypeVarUse]
        ],
    ) -> None:
        """Initialize special attribute and rest from super."""
        attr_name: str = f"_lazy_{getterfunction.__name__}"

        def _lazy_getterfunction(instanceobj: InstanceObjectT) -> ResultT:
            """Check if value present, if not calculate."""
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return cast(ResultT, getattr(instanceobj, attr_name))

        super().__init__(_lazy_getterfunction)


__all__.append("LazyProperty")

ParameterTupleT = TypeVarTuple("ParameterTupleT")


def memoize(
    func: Callable[[Unpack[ParameterTupleT]], ResultT]
) -> Callable[[Unpack[ParameterTupleT]], ResultT]:
    """decorater for caching calls
    thanks to
    <https://towardsdatascience.com/python-decorators-for-data-science-6913f717669a#879f>
    <https://towardsdatascience.com/12-python-decorators-to-take-your-code-to-the-next-level-a910a1ab3e99>
    """
    cache: dict[tuple[Unpack[ParameterTupleT]], ResultT] = {}

    @wraps(func)
    def wrapper(*args: Unpack[ParameterTupleT]) -> ResultT:
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


__all__.append("memoize")
