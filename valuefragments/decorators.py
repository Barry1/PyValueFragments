"""package holding decorators"""


class LazyProperty(property):
    """decorator for properties, which will be only evaluated if needed"""

    def __init__(self, getterfunction):
        attr_name = "_lazy_" + getterfunction.__name__

        def _lazy_getterfunction(instanceobj):
            if not hasattr(instanceobj, attr_name):
                setattr(instanceobj, attr_name, getterfunction(instanceobj))
            return getattr(instanceobj, attr_name)

        super().__init__(_lazy_getterfunction)
