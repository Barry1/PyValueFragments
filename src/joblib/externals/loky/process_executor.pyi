from concurrent.futures import Executor
from typing import Any, Callable, Dict, Optional, Tuple

class ProcessPoolExecutor(Executor):
    def __init__(
        self,
        max_workers: Optional[int],
        job_reducers: Dict,
        result_reducers: Dict,
        timeout: Optional[int],
        context: Any,
        initializer: Callable,
        initargs: Tuple,
        env: Dict,
    ) -> None: ...
    # def shutdown(self, wait: bool = True, kill_workers: bool = False) -> None: ...
    def shutdown(
        self, wait: bool = True, *, cancel_futures: bool = False
    ) -> None: ...
