from concurrent.futures import Executor
from typing import Optional, Any, Callable, Tuple, Dict

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
    def shutdown(self, wait: bool = True, kill_workers: bool = False) -> None: ...
