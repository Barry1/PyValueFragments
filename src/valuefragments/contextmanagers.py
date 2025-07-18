"""Module holding context managers."""

from __future__ import annotations

import os
import sys
from time import monotonic
from types import TracebackType
from typing import AnyStr, BinaryIO, Iterable, Optional, TextIO

from typing_extensions import Literal, Type

from .helpers import closeifrunningloky, ic, print_time_result

# from .moduletools import moduleexport # only working for functions - problem with classes

__all__: list[str] = []


class NoOutput(TextIO):
    """Contextmanager to suppress any output (stderr and stdout)."""

    stdout: TextIO
    stderr: TextIO

    def __enter__(self: "NoOutput") -> "NoOutput":
        """Enter/start context. Save and replace Streams."""
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stderr = self
        sys.stdout = self
        return self

    def __exit__(
        self,
        _exc_type: Optional[Type[BaseException]],
        _exc_value: Optional[BaseException],
        _exc_traceback: Optional[TracebackType],
    ) -> None:
        """Exit the context. Restore Streams."""
        sys.stderr = self.stderr
        sys.stdout = self.stdout

    def write(self: NoOutput, s: AnyStr) -> int:  # pylint: disable=invalid-name,unused-argument
        """Write method: Needed but does nothing."""
        return 0

    def flush(self: NoOutput) -> None:
        """Flush attribute: Needed but does nothing."""

    @property
    def buffer(self: NoOutput) -> BinaryIO:
        """Buffer: Needed but does nothing."""
        return self.buffer

    @property
    def encoding(self: NoOutput) -> str:
        """Encoding: Needed but does nothing."""
        return ""

    # noinspection PyPropertyDefinition
    @property
    def errors(self: NoOutput) -> Optional[str]:
        """Errors: Needed but does nothing."""

    @property
    def line_buffering(self: NoOutput) -> int:
        """Line_buffering: Needed but does nothing."""
        return 0

    # noinspection PyPropertyDefinition
    @property
    def newlines(self: NoOutput) -> None:
        """Newlines: Needed but does nothing."""

    def __iter__(self: NoOutput) -> NoOutput:
        """Only needed for mypy."""
        return self

    def __next__(self: NoOutput) -> str:
        """Only needed for mypy."""
        return ""

    def close(self: NoOutput) -> None:
        """Only needed for mypy."""
        # pass

    def fileno(self: NoOutput) -> int:
        """Only needed for mypy."""
        return -1

    def read(self: NoOutput, _n: int = -1) -> str:
        """Only needed for mypy."""
        return ""

    def isatty(self: NoOutput) -> bool:
        """Only needed for mypy."""
        return False

    def readable(self: NoOutput) -> bool:
        """Only needed for mypy."""
        return False

    def readline(self: NoOutput, _limit: int = -1) -> str:
        """Only needed for mypy."""
        return ""

    def readlines(self: NoOutput, _limit: int = -1) -> list[str]:
        """Only needed for mypy."""
        return []

    def seek(self: NoOutput, _offset: int, _whence: int = 0) -> int:
        """Only needed for mypy."""
        return 0

    def writelines(self: NoOutput, lines: Iterable[str]) -> None:
        """Only needed for mypy."""
        # pass

    def seekable(self: NoOutput) -> bool:
        """Only needed for mypy."""
        return False

    def truncate(self: NoOutput, _size: Optional[int] = None) -> int:
        """Only needed for mypy."""
        return 0

    def writable(self: NoOutput) -> bool:
        """Only needed for mypy."""
        return True

    def tell(self: NoOutput) -> int:
        """Only needed for mypy."""
        return 0


__all__.append("NoOutput")


class LinuxTimeCM:
    """
    Use this as a context manager for getting timing details like with linux time.

    at the moment it is needed to be instantiated with parenthesis as in
    with LinuxTimeCM():
    hopefully I can remove that for further simplification
    """

    before: os.times_result
    after: os.times_result

    def __init__(self) -> None:  # : TimingCM
        """Prepare (type) variables."""
        ic("Prepared to run with LinuxTime -> __init__")

    def __enter__(self: LinuxTimeCM) -> LinuxTimeCM:
        """Save startup timing information."""
        self.before = os.times()
        ic("Prepared to run with LinuxTime -> __enter__")
        return self

    def __exit__(
        self: LinuxTimeCM,
        _exc_type: Optional[Type[BaseException]],
        _exc_value: Optional[BaseException],
        _exc_traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Retrieve end timing information and print."""
        closeifrunningloky()
        self.after = os.times()
        if self.before and self.after:
            print_time_result(
                wall=self.after.elapsed - self.before.elapsed,
                user=self.after.user
                - self.before.user
                + self.after.children_user
                - self.before.children_user,
                system=self.after.system
                - self.before.system
                + self.after.children_system
                - self.before.children_system,
            )
        ic("Ended to run with Timing -> __exit__")
        return True


try:
    import resource

    # resource = __import__("resource")
except ImportError:
    ic("resource is not available")
else:

    class LinuxTimeResourceCM:
        """
        Use this as a context manager for getting timing details like with linux time.

        at the moment it is needed to be instantiated with parenthesis as in
        with LinuxTimeCM():
        hopefully I can remove that for further simplification
        """

        before: float | Literal[0]
        childbefore: resource.struct_rusage
        selfbefore: resource.struct_rusage
        selfafter: resource.struct_rusage
        childafter: resource.struct_rusage
        after: float | Literal[0]

        def __init__(self) -> None:  # : TimingCM
            """Prepare (type) variables."""
            ic("Prepared to run with LinuxTime -> __init__")

        def __enter__(self: LinuxTimeResourceCM) -> LinuxTimeResourceCM:
            """Save startup timing information."""
            self.before = monotonic()
            self.childbefore = resource.getrusage(resource.RUSAGE_CHILDREN)
            self.selfbefore = resource.getrusage(resource.RUSAGE_SELF)
            ic("Prepared to run with LinuxTime -> __enter__")
            return self

        def __exit__(
            self: LinuxTimeResourceCM,
            _exc_type: Optional[Type[BaseException]],
            _exc_value: Optional[BaseException],
            _exc_traceback: Optional[TracebackType],
        ) -> Optional[bool]:
            """Retrieve end timing information and print."""
            closeifrunningloky()
            self.selfafter = resource.getrusage(resource.RUSAGE_SELF)
            self.childafter = resource.getrusage(resource.RUSAGE_CHILDREN)
            self.after = monotonic()
            if all(
                (
                    self.selfbefore,
                    self.selfafter,
                    self.childbefore,
                    self.childafter,
                    self.before,
                    self.after,
                )
            ):
                print_time_result(
                    wall=self.after - self.before,
                    user=self.selfafter.ru_utime
                    - self.selfbefore.ru_utime
                    + self.childafter.ru_utime
                    - self.childbefore.ru_utime,
                    system=self.selfafter.ru_stime
                    - self.selfbefore.ru_stime
                    + self.childafter.ru_stime
                    - self.childbefore.ru_stime,
                )
            ic("Ended to run with Timing -> __exit__")
            return True


class TimingCM:
    """
    Use this as a context manager for getting timing details.

    at the moment it is needed to be instantiated with parenthesis as in
    with TimingCM():
    hopefully I can remove that for further simplification
    """

    # https://book.pythontips.com/en/latest/context_managers.html#implementing-a-context-manager-as-a-class
    # https://www.python.org/dev/peps/pep-0484/ Type hints
    # Instance variables should be type hinted here not in __init__ by
    # <https://www.python.org/dev/peps/pep-0526/#class-and-instance-variable-annotations>
    # pseudo private instance variables with single underscore
    # https://adamj.eu/tech/2021/07/04/python-type-hints-how-to-type-a-context-manager/
    starttimes: os.times_result
    endtimes: os.times_result

    def __init__(self) -> None:  # : TimingCM
        """Prepare (type) variables."""
        ic("Prepared to run with Timing -> __init__")

    def __enter__(self: TimingCM) -> TimingCM:
        """Save startup timing information."""
        # old solution used time: monotonic(), process_time(), thread_time()
        self.starttimes = os.times()
        ic("Prepared to run with Timing -> __enter__")
        return self

    def __exit__(
        self: TimingCM,
        _exc_type: Optional[Type[BaseException]],
        _exc_value: Optional[BaseException],
        _exc_traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Retrieve end timing information and print."""
        closeifrunningloky()
        self.endtimes = os.times()
        timedelta: list[float] = [e - a for (a, e) in zip(self.starttimes, self.endtimes)]
        print(
            f"{timedelta[0] + timedelta[2]:8.2f} [s] User",
            f"{timedelta[1] + timedelta[3]:8.2f} [s] System",
            f"{timedelta[4]:8.2f} [s] Wall",
            f"{sum(timedelta[:4]) / timedelta[4] * 100:8.2f} [%] Load",
        )
        ic("Ended to run with Timing -> __exit__")
        return True
