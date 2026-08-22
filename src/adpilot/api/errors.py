"""Centralized RFC 7807 Problem Details error handling."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..core.config import get_config
from ..core.exceptions import AdPilotError
from ..utils.logging_utils import logger


class ProblemDetails(BaseModel):
    """RFC 7807 Problem Details error model."""

    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: str
    invalid_params: Optional[List[Dict[str, Any]]] = None
    details: Optional[Dict[str, Any]] = None


def create_problem_response(
    status_code: int,
    title: str,
    detail: str,
    request: Request,
    error_code: Optional[str] = None,
    error_type: str = "about:blank",
    invalid_params: Optional[List[Dict[str, Any]]] = None,
    extra_details: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    """Construct an RFC 7807 compliant JSONResponse."""
    request_id = getattr(request.state, "request_id", None) or request.headers.get("X-Request-ID")

    problem = ProblemDetails(
        type=error_type,
        title=title,
        status=status_code,
        detail=detail,
        instance=request_id or str(request.url.path),
        error_code=error_code,
        timestamp=datetime.now(timezone.utc).isoformat(),
        invalid_params=invalid_params,
        details=extra_details,
    )

    headers = {}
    if request_id:
        headers["X-Request-ID"] = request_id

    return JSONResponse(
        status_code=status_code,
        content=problem.model_dump(exclude_none=True),
        headers=headers,
    )


async def adpilot_exception_handler(request: Request, exc: AdPilotError) -> JSONResponse:
    """Handle custom AdPilot domain exceptions."""
    logger.warning(
        "AdPilot domain exception occurred",
        error_code=exc.error_code,
        status_code=exc.status_code,
        message=exc.message,
        path=request.url.path,
    )

    return create_problem_response(
        status_code=exc.status_code,
        title=exc.error_code.replace("_", " ").title(),
        detail=exc.message,
        request=request,
        error_code=exc.error_code,
        extra_details=exc.details if exc.details else None,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI/Starlette HTTPExceptions."""
    logger.warning(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
    )

    titles = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        408: "Request Timeout",
        409: "Conflict",
        422: "Unprocessable Entity",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
    }

    title = titles.get(exc.status_code, "HTTP Error")
    detail_str = exc.detail if isinstance(exc.detail, str) else str(exc.detail)

    return create_problem_response(
        status_code=exc.status_code,
        title=title,
        detail=detail_str,
        request=request,
        error_code=f"HTTP_{exc.status_code}",
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic/FastAPI request validation errors."""
    errors = exc.errors()
    invalid_params: List[Dict[str, Any]] = []

    for err in errors:
        loc = " -> ".join([str(x) for x in err.get("loc", [])])
        invalid_params.append({
            "name": loc,
            "reason": err.get("msg", "Invalid parameter"),
            "type": err.get("type", "value_error"),
        })

    logger.warning(
        "Request validation failed",
        path=request.url.path,
        errors_count=len(errors),
    )

    return create_problem_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        title="Validation Error",
        detail="The request body or parameters failed schema validation.",
        request=request,
        error_code="VALIDATION_ERROR",
        invalid_params=invalid_params,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unhandled exceptions (RFC 7807 500)."""
    logger.error(
        "Unhandled exception in request processing",
        exc_info=exc,
        path=request.url.path,
    )

    config = get_config()
    detail = "An internal server error occurred while processing the request."
    if config.debug or config.environment == "development":
        detail = f"{type(exc).__name__}: {str(exc)}"

    return create_problem_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        title="Internal Server Error",
        detail=detail,
        request=request,
        error_code="INTERNAL_SERVER_ERROR",
    )


def setup_error_handlers(app: FastAPI) -> None:
    """Register all centralized RFC 7807 exception handlers on the FastAPI app."""
    app.add_exception_handler(AdPilotError, adpilot_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
