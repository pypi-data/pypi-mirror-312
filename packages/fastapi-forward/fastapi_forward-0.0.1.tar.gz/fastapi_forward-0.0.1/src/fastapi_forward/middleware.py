"""Request Forwarding Middleware.

This middleware is used to forward requests to different target URLs based on defined rules.
"""

from typing import Callable, Optional

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.routing import compile_path
import httpx


# Store redirect rules
_forward_rules = {}


def add_forward_rule(
    method: str,
    path: str,
    target_base_url: str,
    condition: Optional[Callable[[], bool]] = None,
):
    """Add a redirect rule for specific path.

    Args:
        method: HTTP method that should be redirected
        path: URL path that should be redirected (without prefix)
        target_base_url: Target base URL to redirect to
        condition: Optional condition function that must return True for redirect to occur
    """
    path_regex, path_format, param_converters = compile_path(path)

    _forward_rules[(method, path)] = {
        "target": target_base_url,
        "condition": condition,
        "path_regex": path_regex,
    }


class ForwardMiddleware(BaseHTTPMiddleware):
    """Middleware for forwarding requests to different target URLs."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Dispatch the request and handle forwarding if needed.
        
        Args:
            request (Request): The incoming request
            call_next (RequestResponseEndpoint): The next middleware in the chain
            
        Returns:
            Response: The response from either the forwarded request or the normal chain
        """
        # Preserve request body for potential multiple reads
        body = await request.body()

        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive

        full_path = request.url.path
        method = request.method

        # Find matching redirect rule
        matched_rule = None
        for (rule_method, rule_path), rule in _forward_rules.items():
            if method == rule_method and rule["path_regex"].match(full_path):
                matched_rule = rule
                break

        if matched_rule:
            # Check if condition is met for redirection
            if matched_rule["condition"] is None or matched_rule["condition"]():
                base_url = matched_rule["target"]
            else:
                return await call_next(request)
        else:
            return await call_next(request)

        # Forward request to target URL
        async with httpx.AsyncClient() as client:
            redirect_resp = await client.request(
                request.method,
                f"{base_url}{request.url.path}",
                headers=request.headers,
                content=request.stream(),
            )
        return Response(
            content=redirect_resp.content,
            status_code=redirect_resp.status_code,
            headers=redirect_resp.headers,
        )

def init_app(app: FastAPI):
    """Initialize the request forwarding middleware.
    
    Args:
        app (FastAPI): FastAPI application instance
    """
    # Register redirect rules when the application starts
    @app.on_event("startup")
    async def register_forward_rules():
        for route in app.routes:
            if hasattr(route, "endpoint"):
                endpoint = route.endpoint  # type: ignore
                if hasattr(endpoint, "_register_forward_rule"):
                    endpoint._register_forward_rule(route)

    app.add_middleware(ForwardMiddleware)
