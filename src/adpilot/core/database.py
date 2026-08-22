"""Database connection, connection pool, and session lifecycle management."""

from __future__ import annotations

import time
from typing import AsyncGenerator, Optional, Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import QueuePool

from .config import get_config
from .exceptions import DatabaseConnectionError
from ..utils.logging_utils import logger


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# Global engine and session factory references
_engine: Optional[AsyncEngine] = None
_async_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_engine() -> AsyncEngine:
    """Return or initialize the global AsyncEngine."""
    global _engine
    if _engine is None:
        config = get_config()
        db_url = config.database_url

        engine_kwargs = {
            "echo": config.db_echo or (config.environment == "development" and config.debug),
            "future": True,
        }

        if "sqlite" in db_url:
            # SQLite configuration
            engine_kwargs["connect_args"] = {"check_same_thread": False}
            if ":memory:" in db_url:
                from sqlalchemy.pool import StaticPool
                engine_kwargs["poolclass"] = StaticPool
        else:
            # PostgreSQL / MySQL configuration with QueuePool
            engine_kwargs["poolclass"] = QueuePool
            engine_kwargs["pool_size"] = config.db_pool_size
            engine_kwargs["max_overflow"] = config.db_max_overflow
            engine_kwargs["pool_timeout"] = config.db_pool_timeout
            engine_kwargs["pool_recycle"] = config.db_pool_recycle
            engine_kwargs["pool_pre_ping"] = True

        _engine = create_async_engine(db_url, **engine_kwargs)
        logger.info("Database async engine initialized", url=db_url.split("@")[-1])

    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return or initialize the global async sessionmaker factory."""
    global _async_session_factory
    if _async_session_factory is None:
        engine = get_engine()
        _async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _async_session_factory


# Module-level aliases for backwards compatibility with existing code & tests
class _LazyEngineProxy:
    def __getattr__(self, name):
        return getattr(get_engine(), name)

    def begin(self):
        return get_engine().begin()


class _LazySessionFactoryProxy:
    def __call__(self, *args, **kwargs):
        return get_session_factory()(*args, **kwargs)


engine = _LazyEngineProxy()
async_session_factory = _LazySessionFactoryProxy()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session with automatic transaction management."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def ping_db() -> Tuple[bool, float]:
    """Execute a lightweight query to verify database connectivity and measure latency.
    
    Returns:
        Tuple of (is_healthy, latency_in_ms)
    """
    start_time = time.perf_counter()
    try:
        engine_instance = get_engine()
        async with engine_instance.connect() as conn:
            await conn.execute(text("SELECT 1"))
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return True, latency_ms
    except Exception as exc:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.error("Database ping failed", error=str(exc), latency_ms=latency_ms)
        return False, latency_ms


async def init_db() -> None:
    """Initialize database engine and verify connectivity on startup."""
    is_healthy, latency_ms = await ping_db()
    if not is_healthy:
        config = get_config()
        if config.is_production:
            raise DatabaseConnectionError("Database is unreachable during production startup.")
        logger.warning("Database ping returned unhealthy during initialization.", latency_ms=latency_ms)
    else:
        logger.info("Database connection verified successfully.", latency_ms=latency_ms)


async def close_db() -> None:
    """Gracefully dispose of database connection pools on shutdown."""
    global _engine, _async_session_factory
    if _engine is not None:
        logger.info("Disposing database async engine...")
        await _engine.dispose()
        _engine = None
        _async_session_factory = None
        logger.info("Database async engine disposed.")


async def create_tables() -> None:
    """Create all registered ORM tables if they don't already exist."""
    # Ensure all ORM models are imported so they register in Base.metadata
    from ..models import (  # noqa: F401
        audit_log,
        campaign_publish,
        campaign_task,
        design_asset,
        organization,
        user,
    )

    engine_instance = get_engine()
    async with engine_instance.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database ORM tables verified/created.")
