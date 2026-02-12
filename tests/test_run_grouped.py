"""Async test thread,tpe,ppe.
Attention: Only with PPE (ProcessPoolExecutor) randoms will be reproducible,
as within threads (tpe and thread) it could not be guaranteed.
"""

from collections.abc import Callable
from functools import partial
from math import pi

import pytest

from valuefragments.helpers import pi_for_cpu_load, run_grouped

COUNT: int = 100


tasklist: list[Callable[[], float]] = [
    partial(pi_for_cpu_load, 10000, 4478) for _ in range(COUNT)
]


@pytest.mark.asyncio
async def test_run_grouped_thread() -> None:
    """Fake main routine for async processing."""
    assert (
        abs(sum(await run_grouped(tasklist, "thread"), -COUNT * pi))
        <= pi / 100 * COUNT
    )


@pytest.mark.asyncio
async def test_run_grouped_ppe() -> None:
    """Fake main routine for async processing."""
    assert (
        abs(sum(await run_grouped(tasklist, "ppe"), -COUNT * pi))
        <= pi / 100 * COUNT
    )


@pytest.mark.asyncio
async def test_run_grouped_tpe() -> None:
    """Fake main routine for async processing."""
    assert (
        abs(sum(await run_grouped(tasklist, "tpe"), -COUNT * pi))
        <= pi / 100 * COUNT
    )
