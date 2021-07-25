"""module holding decorators."""
import time

from .helpers import ic  # pylint: disable=E0402

try:
    import resource
except ImportError:
    ic("resource is not available")
else:

    def timing_resource(func):
        """Measure execution times by resource."""
        save = func.__name__

        def wrapped(*args, **kwargs):
            """this is the new implementation"""
            before = resource.getrusage(resource.RUSAGE_SELF)[:2]
            retval = func(*args, **kwargs)
            after = resource.getrusage(resource.RUSAGE_SELF)[:2]
            print(save, sum(after) - sum(before))
            return retval

        return wrapped


try:
    import psutil  # type: ignore[import]
except ImportError:
    ic("psutil is not available")
else:

    def timing_psutil(func):
        """Measures execution times by psutil."""
        save = func.__name__

        def wrapped(*args, **kwargs):
            """this is the new implementation"""
            before = psutil.Process().cpu_times()
            retval = func(*args, **kwargs)
            after = psutil.Process().cpu_times()
            print(save, after - before, sum(after - before))
            return retval

        return wrapped


def timing_thread_time(func):
    """Measures execution times by time (thread)."""
    save = func.__name__

    def wrapped(*args, **kwargs):
        """this is the new implementation"""
        before = time.thread_time()
        retval = func(*args, **kwargs)
        after = time.thread_time()
        print(save, after - before)
        return retval

    return wrapped


def timing_process_time(func):
    """Measures execution times by time (process)."""
    save = func.__name__

    def wrapped(*args, **kwargs):
        """this is the new implementation"""
        before = time.process_time()
        retval = func(*args, **kwargs)
        after = time.process_time()
        print(save, after - before)
        return retval

    return wrapped


class LazyProperty(property):
    """
    Decorator for properties, which will be only evaluated if needed.

    implementation based on ideas given in
    <https://stevenloria.com/lazy-properties>
    """

    # archived under <https://archive.is/8yiRH> and
    # <https://web.archive.org/web/20210514102257/https://stevenloria.com/lazy-properties/>
    # having a look at <https://www.programiz.com/python-programming/property>
    # might also help. Further interesting is
    # <https://stackoverflow.com/questions/7151890#answer-7152065>

    def __init__(self, getterfunction):
        """Initialize special attribute and rest from super."""
        attr_name = "_lazy_" + getterfunction.__name__

        def _lazy_getterfunction(instanceobj):
            """Check if value present, if not calculate"""
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return getattr(instanceobj, attr_name)

        super().__init__(_lazy_getterfunction)
