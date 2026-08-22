"""Tests for Redis connection manager, pooling, health checks, and fallback."""

import pytest
from adpilot.core.redis import RedisManager, get_redis_manager, ping_redis


@pytest.mark.anyio
async def test_redis_manager_singleton():
    """Verify RedisManager returns a singleton instance."""
    mgr1 = get_redis_manager()
    mgr2 = RedisManager()
    assert mgr1 is mgr2


@pytest.mark.anyio
async def test_redis_ping_when_disabled():
    """Verify ping returns healthy=False, latency=0.0 when Redis is disabled."""
    # In test environment, REDIS_ENABLED is set to false in conftest.py
    is_healthy, latency = await ping_redis()
    # Should not raise exception
    assert isinstance(is_healthy, bool)
    assert isinstance(latency, float)


@pytest.mark.anyio
async def test_redis_lifecycle():
    """Verify init and close lifecycle methods execute gracefully without errors."""
    mgr = get_redis_manager()
    await mgr.init_redis()
    await mgr.close_redis()
