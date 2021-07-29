"""Module holding context managers."""
from __future__ import annotations

import time
from types import TracebackType
from typing import Optional, Type

from .helpers import ic  # pylint: disable=E0402


class TimingCM:
    """
    Use this as a context manager for getting timing details.

    at the moment it is need to be instatiated with paranthesis as in
    with TimingCM():
    hopefully I can remove that for further simplification
    """

    # https://book.pythontips.com/en/latest/context_managers.html#implementing-a-context-manager-as-a-class
    # https://www.python.org/dev/peps/pep-0484/ Type hints
    # Instance variables should be type hinted here not in __init__ by
    # <https://www.python.org/dev/peps/pep-0526/#class-and-instance-variable-annotations>
    start_process: float
    end_process: float
    start_thread: float
    end_thread: float
    start_wall: float
    end_wall: float

    def __init__(self: TimingCM) -> None:
        """Prepare (type) variables."""
        ic("Prepared to run with Timing")

    def __enter__(self: TimingCM) -> TimingCM:
        """Save startup timing information."""
        self.start_wall = time.monotonic()  # perf_counter()
        self.start_process = time.process_time()
        self.start_thread = time.thread_time()
        return self

    def __exit__(
        self: TimingCM,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        """Retrieve end timing informationc and print."""
        self.end_wall = time.monotonic()  # perf_counter()
        self.end_process = time.process_time()
        self.end_thread = time.thread_time()
        print(
            f"computed {self.end_process-self.start_process} process seconds",
            f"computed {self.end_thread-self.start_thread} thread seconds",
            f"within {self.end_wall-self.start_wall} wall seconds",
        )
