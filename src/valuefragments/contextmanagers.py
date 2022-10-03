"""Module holding context managers."""
from __future__ import annotations

import sys
import time
from types import TracebackType
from typing import Optional, TextIO, Type

from .helpers import ic  # pylint: disable=relative-beyond-top-level


class NoOutput:
    """Contextmanager to suppress any output (stderr and stdout)."""

    stdout: TextIO
    stderr: TextIO

    def __enter__(self: NoOutput) -> NoOutput:
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stderr = self
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_value, traceback)  -> Optional[bool]:
        sys.stderr = self.stderr
        sys.stdout = self.stdout

    #        if exc_type is not None:
    #            # Do normal exception handling
    #            raise

    def write(self, _x) -> None:
        """Write method needed but does nothing."""
        return

    def flush(self) -> None:
        """Flush attribute needed but does nothing."""
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
    _process: float
    _thread: float
    _wall: float

    def __init__(self) -> None:  # : TimingCM
        """Prepare (type) variables."""
        ic("Prepared to run with Timing -> __init__")

    def __enter__(self: TimingCM) -> TimingCM:  # -> TimingCM
        """Save startup timing information."""
        self._wall = -time.monotonic()
        self._process = -time.process_time()
        self._thread = -time.thread_time()
        ic("Prepared to run with Timing -> __enter__")
        return self

    def __exit__(
        self: TimingCM,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Retrieve end timing information and print."""
        self._wall += time.monotonic()
        self._process += time.process_time()
        self._thread += time.thread_time()
        print(
            f"computed {self._process} process seconds",
            f"and {self._thread} thread seconds",
            f"within {self._wall} wall seconds",
            f"resulting in {100 * self._process / self._wall} % CPU-load.",
        )
        ic("Ended to run with Timing -> __exit__")
        return True
