"""module holding decorators."""
from __future__ import annotations

import sys
import time
# typing with the help of
# <https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators>
from typing import Callable, TypeVar, cast

from .helpers import ic  # pylint: disable=E0402

# https://docs.python.org/3.10/library/typing.html#typing.ParamSpec
if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # pylint: disable=E0611
ParamType = ParamSpec("ParamType")
ResultT = TypeVar("ResultT")
# FunctionTypeVar = TypeVar("FunctionTypeVar", bound=Callable[..., Any])
InstanceObjectT = TypeVar("InstanceObjectT")

# Good info for timinig measurement <https://stackoverflow.com/a/62115793>

try:
    import resource
except ImportError:
    ic("resource is not available")
else:

    def timing_resource(
        func: Callable[ParamType, ResultT]
    ) -> Callable[ParamType, ResultT]:
        """Measure execution times by resource."""
        save: str = func.__name__

        def wrapped(
            *args: ParamType.args,
            **kwargs: ParamType.kwargs,
        ) -> ResultT:
            """Run with timing."""
            before = sum(resource.getrusage(resource.RUSAGE_SELF)[:2])
            retval = func(*args, **kwargs)
            after = sum(resource.getrusage(resource.RUSAGE_SELF)[:2])
            if before and after:
                print(save, after - before)
            return retval

        return wrapped  # cast(FunctionTypeVar, wrapped)


try:
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    def timing_psutil(
        func: Callable[ParamType, ResultT]
    ) -> Callable[ParamType, ResultT]:
        """Measures execution times by psutil."""
        save: str = func.__name__

        def wrapped(
            *args: ParamType.args,
            **kwargs: ParamType.kwargs,
        ) -> ResultT:
            """Run with timing."""
            before: psutil._common.pcputimes = psutil.Process().cpu_times()  # pcputimes
            retval = func(*args, **kwargs)
            after: psutil._common.pcputimes = psutil.Process().cpu_times()
            delta = [end - start for start, end in zip(before, after)]
            print(save, delta, sum(delta))
            return retval

        return wrapped  # cast(FunctionTypeVar, wrapped)


def timing_thread_time(
    func: Callable[ParamType, ResultT]
) -> Callable[ParamType, ResultT]:
    """Measures execution times by time (thread)."""
    save: str = func.__name__

    def wrapped(
        *args: ParamType.args,
        **kwargs: ParamType.kwargs,
    ) -> ResultT:
        """Run with timing."""
        before = time.thread_time()
        retval = func(*args, **kwargs)
        after = time.thread_time()
        print(save, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


def timing_process_time(
    func: Callable[ParamType, ResultT]
) -> Callable[ParamType, ResultT]:
    """Measures execution times by time (process)."""
    save: str = func.__name__

    def wrapped(*args: ParamType.args, **kwargs: ParamType.kwargs) -> ResultT:
        """Run with timing."""
        before = time.process_time()
        retval = func(*args, **kwargs)
        after = time.process_time()
        print(save, after - before)
        return retval

    return wrapped  # cast(FunctionTypeVar, wrapped)


class LazyProperty(property):
    """
    Decorator for properties, which will be only evaluated if needed.

    implementation based on ideas given in
    <https://stevenloria.com/lazy-properties>
    """

    # <https://towardsdatascience.com/2807ef52d273> = <https://archive.is/GfSvY>
    # archived under <https://archive.is/8yiRH> and
    # <https://web.archive.org/web/20210514102257/https://stevenloria.com/lazy-properties/>
    # having a look at <https://www.programiz.com/python-programming/property>
    # might also help. Further interesting is
    # <https://stackoverflow.com/questions/7151890#answer-7152065>
    def __init__(
        self,
        getterfunction: Callable[[InstanceObjectT], ResultT],
    ) -> None:
        """Initialize special attribute and rest from super."""
        attr_name: str = "_lazy_" + getterfunction.__name__

        def _lazy_getterfunction(instanceobj: InstanceObjectT) -> ResultT:
            """Check if value present, if not calculate."""
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return cast(ResultT, getattr(instanceobj, attr_name))

        super().__init__(_lazy_getterfunction)
