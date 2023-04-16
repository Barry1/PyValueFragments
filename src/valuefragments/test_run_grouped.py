"""async test thread,tpe,ppe."""
import sys

import pytest

if sys.version_info >= (3, 11):
    import asyncio
    from functools import partial

    from .contextmanagers import LinuxTimeCM
    from .helpers import pi_for_cpu_load, run_grouped

    tasklist = [partial(pi_for_cpu_load, 10000000, 4478) for _ in range(5)]

    @pytest.mark.asyncio
    async def test_run_grouped_thread() -> None:
        """Fake main routine for async processing."""
        assert sum(await run_grouped(tasklist, "thread")) == 5 * 3.1413716

    @pytest.mark.asyncio
    async def test_run_grouped_ppe() -> None:
        """Fake main routine for async processing."""
        assert sum(await run_grouped(tasklist, "ppe")) == 5 * 3.1413716

    @pytest.mark.asyncio
    async def test_run_grouped_tpe() -> None:
        """Fake main routine for async processing."""
        assert sum(await run_grouped(tasklist, "tpe")) == 5 * 3.1413716
