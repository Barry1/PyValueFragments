from .process_executor import ProcessPoolExecutor

__all__ = ["get_reusable_executor"]
_executor_lock = threading.RLock()
from typing import Any, Callable, Dict, Tuple

def get_reusable_executor(
    max_workers: int = None,
    context=Any,
    timeout: int = 10,
    kill_workers: bool = False,
    reuse: str = "auto",
    job_reducers=Dict,
    result_reducers=Dict,
    initializer=Callable,
    initargs: Tuple = (),
    env=Dict,
) -> _ReusablePoolExecutor: ...

class _ReusablePoolExecutor(ProcessPoolExecutor): ...
