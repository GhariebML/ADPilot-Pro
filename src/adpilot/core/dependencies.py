"""Dependency validation and health check utilities."""

from __future__ import annotations

from typing import Dict, List, Tuple

from .config import get_config
from .database import ping_db
from .redis import ping_redis


async def check_all_dependencies() -> Tuple[bool, Dict[str, bool], List[str]]:
    """Verify all system dependencies and return overall status, per-dependency status, and messages.

    Returns:
        Tuple of (all_critical_ok, dependency_status_map, issue_messages)
    """
    config = get_config()
    status_map: Dict[str, bool] = {}
    issues: List[str] = []

    # 1. Database
    db_ok, db_lat = await ping_db()
    status_map["database"] = db_ok
    if not db_ok:
        issues.append("Primary database connection failed.")

    # 2. Redis
    if config.redis_enabled:
        redis_ok, redis_lat = await ping_redis()
        status_map["redis"] = redis_ok
        if not redis_ok and config.is_production:
            issues.append("Redis connection failed in production.")

    # 3. Memory Service
    try:
        from .container import get_container
        container = get_container()
        _ = container.memory_service
        status_map["memory"] = True
    except Exception as exc:
        status_map["memory"] = False
        issues.append(f"MemoryService initialization failed: {exc}")

    # 4. Vector Store / RAG Service
    try:
        from .container import get_container
        container = get_container()
        _ = container.vector_store
        status_map["vector_store"] = True
    except Exception as exc:
        status_map["vector_store"] = False
        issues.append(f"Vector store initialization failed: {exc}")

    all_critical_ok = status_map.get("database", False)
    return all_critical_ok, status_map, issues
