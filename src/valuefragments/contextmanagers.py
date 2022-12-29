"""Module holding context managers."""
from __future__ import annotations

import os
import sys
from types import TracebackType
from typing import Any, Optional, Self, TextIO, Type

from .helpers import ic  # pylint: disable=relative-beyond-top-level


class NoOutput(TextIO):  # pylint: disable=W0223
    """Contextmanager to suppress any output (stderr and stdout)."""

    stdout: TextIO
    stderr: TextIO

    def __enter__(self: Self) -> Self:  # type: ignore[valid-type]
        """Enter/start context. Save and replace Streams."""
        self.stdout = sys.stdout  # type: ignore[attr-defined]
        self.stderr = sys.stderr  # type: ignore[attr-defined]
        sys.stderr = self
        sys.stdout = self
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        """Exit the context. Restore Streams."""
        sys.stderr = self.stderr
        sys.stdout = self.stdout

    def write(self: Self, _x: Any) -> int:  # type: ignore[valid-type]
        """Write method: Needed but does nothing."""
        return 0

    def flush(self: Self) -> None:  # type: ignore[valid-type]
        """Flush attribute: Needed but does nothing."""
        return


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

    def __enter__(self: Self) -> Self:  # type: ignore[valid-type]
        """Save startup timing information."""
        # old solution used time: monotonic(), process_time(), thread_time()
        self.starttimes = os.times()  # type: ignore[attr-defined]
        ic("Prepared to run with Timing -> __enter__")
        return self

    def __exit__(
        self: Self,  # type: ignore[valid-type]
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Retrieve end timing information and print."""
        # Check if any (loky) backend is still open and if, close
        # pylint C0415==import-outside-toplevel
        try:
            # pylint: disable=C0415
            from joblib.externals.loky import (  # type: ignore[import]
                get_reusable_executor,  # pyright: ignore[reportUnknownVariableType]
            )
        except ModuleNotFoundError:
            pass
        else:
            get_reusable_executor().shutdown()  # pyright: ignore[reportUnknownMemberType]
        self.endtimes = os.times()  # type: ignore[attr-defined]
        timedelta: list[float] = [
            e - a for (a, e) in zip(self.starttimes, self.endtimes)  # type: ignore[attr-defined]
        ]
        #        self._wall += time.monotonic()
        #        self._process += time.process_time()
        #        self._thread += time.thread_time()
        #        print(
        #            f"computed {self._process} process seconds",
        #            f"and {self._thread} thread seconds",
        #            f"within {self._wall} wall seconds",
        #            f"resulting in {100 * self._process / self._wall} % CPU-load.",
        #        )
        print(
            f"{timedelta[0] + timedelta[2]:8.2f} [s] User",
            f"{timedelta[1] + timedelta[3]:8.2f} [s] System",
            f"{timedelta[4]:8.2f} [s] Wall",
            f"{sum(timedelta[:4]) / timedelta[4] * 100 :8.2f} [%] Load",
        )
        ic("Ended to run with Timing -> __exit__")
        return True
