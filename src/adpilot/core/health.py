"""Health check and readiness probe diagnostic services."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .config import get_config
from .database import ping_db
from .redis import ping_redis


class HealthStatus(str, Enum):
    """Health check status levels."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ComponentHealth(BaseModel):
    """Health status and diagnostic telemetry for an individual component."""

    name: str
    status: HealthStatus
    latency_ms: Optional[float] = None
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class HealthReport(BaseModel):
    """Aggregate health and readiness assessment report."""

    status: HealthStatus
    app_name: str
    version: str
    environment: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    components: Dict[str, ComponentHealth] = Field(default_factory=dict)


async def check_liveness() -> Dict[str, Any]:
    """Lightweight liveness probe ensuring the web server process is responsive."""
    config = get_config()
    return {
        "status": "ok",
        "app": config.app_name,
        "version": config.app_version,
        "environment": config.environment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def check_readiness() -> HealthReport:
    """Readiness probe evaluating critical dependencies required to process traffic.

    If any critical dependency (e.g. primary database) fails, returns an UNHEALTHY status.
    """
    config = get_config()
    components: Dict[str, ComponentHealth] = {}
    overall_status = HealthStatus.HEALTHY

    # 1. Database Check (Critical)
    db_healthy, db_latency = await ping_db()
    components["database"] = ComponentHealth(
        name="database",
        status=HealthStatus.HEALTHY if db_healthy else HealthStatus.UNHEALTHY,
        latency_ms=db_latency,
        message="Database connected and responsive." if db_healthy else "Database connection ping failed.",
    )
    if not db_healthy:
        overall_status = HealthStatus.UNHEALTHY

    # 2. Redis Check (Optional/Degraded)
    if config.redis_enabled:
        redis_healthy, redis_latency = await ping_redis()
        components["redis"] = ComponentHealth(
            name="redis",
            status=HealthStatus.HEALTHY if redis_healthy else HealthStatus.DEGRADED,
            latency_ms=redis_latency,
            message="Redis connected and responsive." if redis_healthy else "Redis connection unavailable (fallback active).",
        )
        if not redis_healthy and config.is_production:
            overall_status = HealthStatus.DEGRADED if overall_status != HealthStatus.UNHEALTHY else overall_status

    return HealthReport(
        status=overall_status,
        app_name=config.app_name,
        version=config.app_version,
        environment=config.environment,
        components=components,
    )


async def check_deep_health() -> HealthReport:
    """Comprehensive diagnostics evaluating all services, stores, and integrations."""
    readiness = await check_readiness()
    components = readiness.components
    config = get_config()

    # 3. Vector Store (Qdrant) Check
    try:
        from ..core.container import get_container
        container = get_container()
        _ = container.vector_store
        components["vector_store"] = ComponentHealth(
            name="vector_store",
            status=HealthStatus.HEALTHY,
            message=f"Vector store active in mode: {config.qdrant_mode}",
            details={"mode": config.qdrant_mode, "path": config.qdrant_path if config.qdrant_mode == "local" else config.qdrant_url},
        )
    except Exception as exc:
        components["vector_store"] = ComponentHealth(
            name="vector_store",
            status=HealthStatus.DEGRADED,
            message=f"Vector store diagnostic check failed: {exc}",
        )

    # 4. LLM Provider Configuration Check
    provider = config.llm_provider
    key_configured = False
    if provider == "openrouter" and config.openrouter_api_key:
        key_configured = True
    elif provider == "openai" and config.openai_api_key:
        key_configured = True
    elif provider == "anthropic" and config.anthropic_api_key:
        key_configured = True
    elif provider == "ollama":
        key_configured = True
    elif provider == "huggingface" and config.hf_token:
        key_configured = True

    components["llm_provider"] = ComponentHealth(
        name="llm_provider",
        status=HealthStatus.HEALTHY if key_configured else HealthStatus.DEGRADED,
        message=f"Active provider '{provider}' is {'configured' if key_configured else 'missing API key (demo mode active)'}.",
        details={"provider": provider},
    )

    return HealthReport(
        status=readiness.status,
        app_name=config.app_name,
        version=config.app_version,
        environment=config.environment,
        components=components,
    )
