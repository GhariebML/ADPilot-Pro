"""Redis connection, connection pooling, and lifecycle management."""

from __future__ import annotations

import time
from typing import Optional, Tuple

from redis.asyncio import ConnectionPool, Redis

from .config import get_config
from .exceptions import RedisConnectionError
from ..utils.logging_utils import logger


class RedisManager:
    """Manages async Redis connection pool and provides health checks."""

    _instance: Optional[RedisManager] = None
    _pool: Optional[ConnectionPool] = None
    _client: Optional[Redis] = None

    def __new__(cls) -> RedisManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def is_enabled(self) -> bool:
        return get_config().redis_enabled

    def get_pool(self) -> Optional[ConnectionPool]:
        """Return or create the connection pool."""
        if not self.is_enabled:
            return None

        if self._pool is None:
            config = get_config()
            self._pool = ConnectionPool.from_url(
                config.redis_url,
                max_connections=config.redis_max_connections,
                socket_timeout=config.redis_socket_timeout,
                decode_responses=True,
            )
            logger.info("Redis connection pool created", url=config.redis_url)
        return self._pool

    def get_client(self) -> Optional[Redis]:
        """Return an active async Redis client instance."""
        if not self.is_enabled:
            return None

        if self._client is None:
            pool = self.get_pool()
            if pool:
                self._client = Redis(connection_pool=pool)
        return self._client

    async def ping(self) -> Tuple[bool, float]:
        """Ping the Redis server and measure round-trip latency.

        Returns:
            Tuple of (is_healthy, latency_in_ms)
        """
        if not self.is_enabled:
            return False, 0.0

        start_time = time.perf_counter()
        try:
            client = self.get_client()
            if client is None:
                return False, 0.0
            await client.ping()
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return True, latency_ms
        except Exception as exc:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.warning("Redis ping failed", error=str(exc), latency_ms=latency_ms)
            return False, latency_ms

    async def init_redis(self) -> None:
        """Verify Redis connectivity during startup."""
        if not self.is_enabled:
            logger.info("Redis is disabled by configuration.")
            return

        is_healthy, latency_ms = await self.ping()
        if is_healthy:
            logger.info("Redis connection verified successfully", latency_ms=latency_ms)
        else:
            config = get_config()
            if config.is_production:
                raise RedisConnectionError("Redis is unreachable during production startup.")
            logger.warning(
                "Redis connection failed during startup. Worker queues will fall back to local asyncio execution.",
                latency_ms=latency_ms,
            )

    async def close_redis(self) -> None:
        """Close Redis client and connection pool during shutdown."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
        if self._pool is not None:
            await self._pool.disconnect()
            self._pool = None
        logger.info("Redis connections closed.")


_redis_manager = RedisManager()


def get_redis_manager() -> RedisManager:
    """Return the global RedisManager singleton."""
    return _redis_manager


async def get_redis_client() -> Optional[Redis]:
    """Dependency / helper for retrieving the active async Redis client."""
    return _redis_manager.get_client()


async def ping_redis() -> Tuple[bool, float]:
    """Helper to check Redis health."""
    return await _redis_manager.ping()
