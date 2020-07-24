import functools
import logging
import sys


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except Exception as e:
                    raise Exception(f'Failed example: {new_args[1]}').with_traceback(e.__traceback__)

        return wrapper

    return decorator
