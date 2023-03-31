"""Module holding context managers."""
from __future__ import annotations

import os
import sys
from abc import ABC
from types import TracebackType
from typing import Any, Optional, TextIO, Type

# from typing_extensions import Self
from .helpers import ic  # pylint: disable=relative-beyond-top-level]


class NoOutput(TextIO, ABC):
    """Contextmanager to suppress any output (stderr and stdout)."""

    stdout: TextIO
    stderr: TextIO

    def __enter__(self: NoOutput) -> NoOutput:
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

    def write(self: NoOutput, s: Any) -> int:  # pylint: disable=invalid-name,unused-argument
        """Write method: Needed but does nothing."""
        return 0

    def flush(self: NoOutput) -> None:
        """Flush attribute: Needed but does nothing."""


class TimingCM:  # pyre-ignore[13]
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
        # Check if any (loky) backend is still open and if, close

        try:
            # pylint: disable=import-outside-toplevel
            from joblib.externals.loky import get_reusable_executor
        except ModuleNotFoundError:
            pass
        else:
            get_reusable_executor().shutdown()
        self.endtimes = os.times()
        timedelta: list[float] = [e - a for (a, e) in zip(self.starttimes, self.endtimes)]
        print(
            f"{timedelta[0] + timedelta[2]:8.2f} [s] User",
            f"{timedelta[1] + timedelta[3]:8.2f} [s] System",
            f"{timedelta[4]:8.2f} [s] Wall",
            f"{sum(timedelta[:4]) / timedelta[4] * 100 :8.2f} [%] Load",
        )
        ic("Ended to run with Timing -> __exit__")
        return True
