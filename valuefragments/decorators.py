"""module holding decorators"""
from .helpers import ic  # pylint: disable=E0402

try:
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    def timing_psutil(func):
        """decorator which measures execution times with the help of psutil"""
        save = func.__name__

        def wrapped(*args, **kwargs):
            before = psutil.Process().cpu_times()
            retval = func(*args, **kwargs)
            after = psutil.Process().cpu_times()
            print(save, after - before, sum(after - before))
            return retval

        return wrapped


class LazyProperty(property):
    """
    decorator for properties, which will be only evaluated if needed

    implementation based on ideas given in
    <https://stevenloria.com/lazy-properties>
    """

    # archived under <https://archive.is/8yiRH> and
    # <https://web.archive.org/web/20210514102257/https://stevenloria.com/lazy-properties/>
    # having a look at <https://www.programiz.com/python-programming/property>
    # might also help. Further interesting is
    # <https://stackoverflow.com/questions/7151890#answer-7152065>

    def __init__(self, getterfunction):
        attr_name = "_lazy_" + getterfunction.__name__

        def _lazy_getterfunction(instanceobj):
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return getattr(instanceobj, attr_name)

        super().__init__(_lazy_getterfunction)
