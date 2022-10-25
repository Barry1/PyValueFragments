"""
This type stub file was generated by pyright.
"""

from concurrent.futures import ALL_COMPLETED, CancelledError, Executor, FIRST_COMPLETED, FIRST_EXCEPTION, TimeoutError, as_completed, wait
from .reusable_executor import get_reusable_executor
from .process_executor import ProcessPoolExecutor

__all__ = ["get_reusable_executor",
           "wait",
           "as_completed",
           "Executor",
           "ProcessPoolExecutor",
           "CancelledError",
           "TimeoutError",
           "FIRST_COMPLETED",
           "FIRST_EXCEPTION",
           "ALL_COMPLETED",
           "set_loky_pickler"]
__version__ = ...