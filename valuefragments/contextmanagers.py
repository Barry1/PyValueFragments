"""module holding context managers"""


import time


from .helpers import ic  # pylint: disable=E0402


class TimingCM:
    """use this as a context manager for getting timing details"""

    # https://book.pythontips.com/en/latest/context_managers.html#implementing-a-context-manager-as-a-class
    def __init__(self):
        self.end_cpu = None
        self.end_wall = None
        self.start_cpu = None
        self.start_wall = None
        ic("Prepared to run with Timing")

    def __enter__(self):
        self.start_wall = time.monotonic()  # perf_counter()
        self.start_cpu = time.process_time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end_wall = time.monotonic()  # perf_counter()
        self.end_cpu = time.process_time()
        print(
            f"computed {self.end_cpu-self.start_cpu} cpu seconds",
            f"within {self.end_wall-self.start_wall} wall seconds",
        )
