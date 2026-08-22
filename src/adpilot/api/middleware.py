"""HTTP middleware components for request tracking, logging, and security."""

from __future__ import annotations

import time
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..core.config import get_config
from ..utils.logging_utils import bind_contextvars, clear_contextvars, logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Assigns or propagates a correlation ID for every incoming request and binds to structlog."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        config = get_config()
        header_name = config.correlation_id_header

        request_id = request.headers.get(header_name) or uuid4().hex
        request.state.request_id = request_id

        # Bind request_id to structured logging context
        bind_contextvars(request_id=request_id)

        try:
            response = await call_next(request)
            response.headers[header_name] = request_id
            return response
        finally:
            clear_contextvars()


class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    """Logs HTTP request details, execution time, and response status codes."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            # Avoid logging noisy health checks at INFO level in production
            if path in ("/healthz", "/ready") and response.status_code == 200:
                logger.debug("HTTP request completed", method=method, path=path, status=response.status_code, duration_ms=duration_ms)
            else:
                logger.info("HTTP request completed", method=method, path=path, status=response.status_code, duration_ms=duration_ms)

            response.headers["X-Response-Time"] = f"{duration_ms}ms"
            return response
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error("HTTP request raised unhandled exception", method=method, path=path, error=str(exc), duration_ms=duration_ms)
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Enforces standard security HTTP headers across all responses."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


def setup_middlewares(app: FastAPI) -> None:
    """Register all standard middlewares with the FastAPI application."""
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(HTTPLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
