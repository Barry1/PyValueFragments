"""async test thread,tpe,ppe."""
import asyncio

import pytest

from .contextmanagers import LinuxTimeCM
from .helpers import run_grouped

# from .helpers import run_grouped


def cpu_bound():
    """Just generate CPU load."""
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10**7))


#    import os
#    import threading
#    print(f"PID: {os.getpid()} TID: {threading.get_native_id()} started.")
#    print(f"PID: {os.getpid()} TID: {threading.get_native_id()} ended.")


@pytest.mark.asyncio
async def test_run_grouped_thread() -> None:
    """Fake main routine for async processing."""
    assert await run_grouped([cpu_bound for _ in range(2)], "thread") == [
        333333283333335000000,
        333333283333335000000,
    ]


@pytest.mark.asyncio
async def test_run_grouped_ppe() -> None:
    """Fake main routine for async processing."""
    assert await run_grouped([cpu_bound for _ in range(2)], "ppe") == [
        333333283333335000000,
        333333283333335000000,
    ]


@pytest.mark.asyncio
async def test_run_grouped_tpe() -> None:
    """Fake main routine for async processing."""
    assert await run_grouped([cpu_bound for _ in range(2)], "tpe") == [
        333333283333335000000,
        333333283333335000000,
    ]
