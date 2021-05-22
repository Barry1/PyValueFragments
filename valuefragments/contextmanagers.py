"""module holding context managers"""


import time


from .helpers import ic  # pylint: disable=E0402


class TimingCM:
    """use this as a context manager for getting timing details"""

    # https://book.pythontips.com/en/latest/context_managers.html#implementing-a-context-manager-as-a-class
    def __init__(self):
        self.end_process: float
        self.end_thread: float
        self.end_wall: float
        self.start_process: float
        self.start_thread: float
        self.start_wall: float
        ic("Prepared to run with Timing")

    def __enter__(self):
        self.start_wall = time.monotonic()  # perf_counter()
        self.start_process = time.process_time()
        self.start_thread = time.thread_time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end_wall = time.monotonic()  # perf_counter()
        self.end_process = time.process_time()
        self.end_thread = time.thread_time()
        print(
            f"computed {self.end_process-self.start_process} process seconds",
            f"computed {self.end_thread-self.start_thread} thread seconds",
            f"within {self.end_wall-self.start_wall} wall seconds",
        )
