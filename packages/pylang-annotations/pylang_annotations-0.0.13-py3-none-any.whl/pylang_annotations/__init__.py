def native(arg=None, /):
    return arg if callable(arg) else lambda func: func


def pure(func, /):
    return func


skip_module: object
