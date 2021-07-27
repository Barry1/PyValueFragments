"""module holding decorators."""
from __future__ import annotations

import time

# typing with the help of
# <https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators>
from typing import Any, Callable, TypeVar, cast

from typing_extensions import ParamSpec

from .helpers import ic  # pylint: disable=E0402

ParamType = ParamSpec("ParamType")
ResultType = TypeVar("ResultType")
FunctionTypeVar = TypeVar("FunctionTypeVar", bound=Callable[..., Any])
InstanceObjectType = TypeVar("InstanceObjectType")

try:
    import resource
except ImportError:
    ic("resource is not available")
else:

    def timing_resource(
        func: Callable[ParamType, ResultType]  # type: ignore[misc]
    ) -> Callable[ParamType, ResultType]:  # type: ignore[misc]
        """Measure execution times by resource."""
        save = func.__name__

        # type: ignore[name-defined]
        def wrapped(*args: ParamType.args, **kwargs: ParamType.kwargs) -> ResultType:
            """Run with timing."""
            before = resource.getrusage(resource.RUSAGE_SELF)[:2]
            retval = func(*args, **kwargs)
            after = resource.getrusage(resource.RUSAGE_SELF)[:2]
            print(save, sum(after) - sum(before))
            return retval  # type: ignore[no-any-return]

        return wrapped  # cast(FunctionTypeVar, wrapped)


try:
    import psutil  # type: ignore[import]
except ImportError:
    ic("psutil is not available")
else:

    def timing_psutil(
        func: Callable[ParamType, ResultType]  # type: ignore[misc]
    ) -> Callable[ParamType, ResultType]:  # type: ignore[misc]
        """Measures execution times by psutil."""
        save = func.__name__

        # type: ignore[name-defined]
        def wrapped(*args: ParamType.args, **kwargs: ParamType.kwargs) -> ResultType:
            """Run with timing."""
            before = psutil.Process().cpu_times()
            retval = func(*args, **kwargs)
            after = psutil.Process().cpu_times()
            print(save, after - before, sum(after - before))
            return retval  # type: ignore[no-any-return]

        return wrapped  # cast(FunctionTypeVar, wrapped)


def timing_thread_time(
    func: Callable[ParamType, ResultType]  # type: ignore[misc]
) -> Callable[ParamType, ResultType]:  # type: ignore[misc]
    """Measures execution times by time (thread)."""
    save = func.__name__

    # type: ignore[name-defined]
    def wrapped(*args: ParamType.args, **kwargs: ParamType.kwargs) -> ResultType:
        """Run with timing."""
        before = time.thread_time()
        retval = func(*args, **kwargs)
        after = time.thread_time()
        print(save, after - before)
        return retval  # type: ignore[no-any-return]

    return wrapped  # cast(FunctionTypeVar, wrapped)


def timing_process_time(
    func: Callable[ParamType, ResultType]  # type: ignore[misc]
) -> Callable[ParamType, ResultType]:  # type: ignore[misc]
    """Measures execution times by time (process)."""
    save = func.__name__

    # type: ignore[name-defined]
    def wrapped(*args: ParamType.args, **kwargs: ParamType.kwargs) -> ResultType:
        """Run with timing."""
        before = time.process_time()
        retval = func(*args, **kwargs)
        after = time.process_time()
        print(save, after - before)
        return retval  # type: ignore[no-any-return]

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
        getterfunction: Callable[
            [InstanceObjectType], ResultType  # type: ignore[invalid-type-var-use]
        ],  # type: ignore[invalid-type-var-use]
    ) -> None:
        """Initialize special attribute and rest from super."""
        attr_name = "_lazy_" + getterfunction.__name__

        def _lazy_getterfunction(instanceobj: InstanceObjectType) -> ResultType:
            """Check if value present, if not calculate."""
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return cast(ResultType, getattr(instanceobj, attr_name))

        super().__init__(_lazy_getterfunction)
