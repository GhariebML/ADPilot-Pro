import os
os.environ["QDRANT_PATH"] = "./storage/test_qdrant_db"
os.environ["ENVIRONMENT"] = "test"
os.environ["REDIS_ENABLED"] = "false"

import asyncio
import pytest
from adpilot.core.database import Base, get_engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Session-scoped fixture to cleanly drop and recreate all SQL tables."""
    async def _setup():
        eng = get_engine()
        async with eng.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            
    asyncio.run(_setup())
    yield


@pytest.fixture
def anyio_backend():
    """Ensure anyio tests run with standard asyncio backend."""
    return "asyncio"
