import functools
from typing import Any
from typing import Callable

from flask import abort
from flask import request


def json_required() -> Callable:
    """Check if the request content-type is json otherwise abort."""

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not request.is_json:
                abort(406)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
