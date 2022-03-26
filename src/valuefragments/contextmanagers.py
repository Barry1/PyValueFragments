"""Module holding context managers."""
from __future__ import annotations

import time
from types import TracebackType
from typing import Optional, Type

from .helpers import ic  # pylint: disable=E0402


class TimingCM:  # pyre-ignore[13]
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
    # pseudo private intance variables with single underscore
    # https://adamj.eu/tech/2021/07/04/python-type-hints-how-to-type-a-context-manager/
    _process: float
    _thread: float
    _wall: float

    def __init__(self: TimingCM) -> None:
        """Prepare (type) variables."""
        # self._process:float# = 0
        # self._thread:float# = 0
        # self._wall:float# = 0
        ic("Prepared to run with Timing -> __init__")

    def __enter__(self: TimingCM) -> None:  # -> TimingCM
        """Save startup timing information."""
        self._wall = -time.monotonic()
        self._process = -time.process_time()
        self._thread = -time.thread_time()
        ic("Prepared to run with Timing -> __enter__")
        # return self

    def __exit__(
        self: TimingCM,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        """Retrieve end timing informationc and print."""
        self._wall += time.monotonic()
        self._process += time.process_time()
        self._thread += time.thread_time()
        print(
            f"computed {self._process} process seconds",
            f"and {self._thread} thread seconds",
            f"within {self._wall} wall seconds",
            f"resulting in {100*(self._process)/(self._wall)} % CPU-load.",
        )
        ic("Ended to run with Timing -> __exit__")
