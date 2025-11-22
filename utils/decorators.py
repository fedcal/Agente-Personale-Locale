import time
from functools import wraps
from typing import Callable, Any


def timeit(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            duration = (time.time() - start) * 1000
            print(f"{func.__name__} completato in {duration:.1f}ms")
    return wrapper
