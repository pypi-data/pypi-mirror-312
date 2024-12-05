from fastapi.routing import APIRoute
from typing import Callable
from functools import wraps
import inspect
from fastapi_forward.middleware import add_forward_rule


def forward(target_base_url: str, condition: Callable[[], bool] | None = None):
    """Request forwarding decorator.

    Used to forward requests to a specified base URL.

    Args:
        target_base_url: The target base URL to forward requests to
        condition: Optional condition function that returns True when forwarding should occur
    """

    def decorator(func):
        original_func = func

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if inspect.iscoroutinefunction(original_func):
                return await original_func(*args, **kwargs)
            return original_func(*args, **kwargs)

        def register_forward_rule(route: APIRoute):
            full_path = route.path

            if not full_path.startswith("/"):
                full_path = "/" + full_path

            for method in route.methods:
                add_forward_rule(
                    method,
                    full_path,
                    target_base_url,
                    condition,
                )

        setattr(wrapper, "_register_forward_rule", register_forward_rule)
        return wrapper

    return decorator