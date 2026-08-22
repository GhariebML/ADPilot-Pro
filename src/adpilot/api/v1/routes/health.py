"""Health check, readiness, and diagnostics API routes."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Response, status

from ....core.health import (
    HealthReport,
    HealthStatus,
    check_deep_health,
    check_liveness,
    check_readiness,
)

router = APIRouter(tags=["Health & Diagnostics"])


@router.get("/healthz", summary="Liveness Probe", status_code=status.HTTP_200_OK)
async def liveness_probe() -> Dict[str, Any]:
    """Lightweight liveness probe returning HTTP 200 as long as the server is running."""
    return await check_liveness()


@router.get("/ready", summary="Readiness Probe", response_model=HealthReport)
async def readiness_probe(response: Response) -> HealthReport:
    """Readiness probe verifying core dependencies (Database, Redis).
    
    Returns HTTP 200 when ready to accept traffic, or HTTP 503 if critical dependencies are down.
    """
    report = await check_readiness()
    if report.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return report


@router.get("/health", summary="Deep System Diagnostics", response_model=HealthReport)
async def deep_health_check(response: Response) -> HealthReport:
    """Comprehensive diagnostic endpoint checking database, redis, vector store, and LLM configuration."""
    report = await check_deep_health()
    if report.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return report
