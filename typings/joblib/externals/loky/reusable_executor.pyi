"""
This type stub file was generated by pyright.
"""

from .process_executor import ProcessPoolExecutor


class _ReusablePoolExecutor(ProcessPoolExecutor):
    def __init__(self, submit_resize_lock, max_workers=..., context=..., timeout=..., executor_id=..., job_reducers=..., result_reducers=..., initializer=..., initargs=..., env=...) -> None:
        ...
    
    @classmethod
    def get_reusable_executor(cls, max_workers=..., context=..., timeout=..., kill_workers=..., reuse=..., job_reducers=..., result_reducers=..., initializer=..., initargs=..., env=...) -> tuple[Self@_ReusablePoolExecutor, bool]:
        ...
    
    def submit(self, fn, *args, **kwargs): # -> Future:
        ...

def get_reusable_executor(max_workers=..., context=..., timeout=..., kill_workers=..., reuse=..., job_reducers=..., result_reducers=..., initializer=..., initargs=..., env=...) -> _ReusablePoolExecutor:
    

