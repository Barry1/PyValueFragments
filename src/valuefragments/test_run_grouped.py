"""Async test thread,tpe,ppe.
Attention: Only with PPE (ProcessPoolExecutor) randoms will be reproducible,
as within threads (tpe and thread) it could not be guaranteed.
"""

import sys

import pytest

if sys.version_info >= (3, 11):
    from functools import partial

    from .helpers import pi_for_cpu_load, run_grouped

    tasklist: list[partial[float]] = [partial(pi_for_cpu_load, 10000, 4478) for _ in range(5)]

    @pytest.mark.asyncio
    async def test_run_grouped_thread() -> None:
        """Fake main routine for async processing."""
        assert abs(sum(await run_grouped(tasklist, "thread"), -15.638000000000002)) <= 0.04

    @pytest.mark.asyncio
    async def test_run_grouped_ppe() -> None:
        """Fake main routine for async processing."""
        assert sum(await run_grouped(tasklist, "ppe")) == 15.638000000000002

    @pytest.mark.asyncio
    async def test_run_grouped_tpe() -> None:
        """Fake main routine for async processing."""
        localtasklist: list[partial[float]] = [
            partial(pi_for_cpu_load, 10000, 4478) for _ in range(5)
        ]
        assert abs(sum(await run_grouped(localtasklist, "tpe"), -15.638000000000002)) <= 0.04
