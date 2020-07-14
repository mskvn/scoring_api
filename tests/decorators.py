import functools

def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except Exception as e:
                    raise type(e)(str(e) + f'\nFailed example: {new_args[1]}'
                                  ).with_traceback(sys.exc_info()[2])

        return wrapper

    return decorator