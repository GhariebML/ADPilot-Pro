"""Tests for database engine lifecycle, connection ping, session management, and rollback."""

import pytest
from sqlalchemy import text
from adpilot.core.database import (
    get_db_session,
    ping_db,
)
from adpilot.models.user import User


@pytest.mark.anyio
async def test_database_ping():
    """Verify database ping executes successfully and measures latency."""
    is_healthy, latency_ms = await ping_db()
    assert is_healthy is True
    assert latency_ms >= 0.0


@pytest.mark.anyio
async def test_session_commit_and_query():
    """Verify async database session commits and reads records."""
    async for session in get_db_session():
        user = User(
            id="test-db-user",
            email="dbuser@example.com",
            hashed_password="hashed_pwd",
            role="marketer",
        )
        session.add(user)
        # Commit happens automatically at end of get_db_session context

    async for session in get_db_session():
        result = await session.execute(text("SELECT email FROM users WHERE id = 'test-db-user'"))
        row = result.fetchone()
        assert row is not None
        assert row[0] == "dbuser@example.com"


@pytest.mark.anyio
async def test_session_rollback_on_exception():
    """Verify session automatically rolls back transaction when an exception is raised."""
    try:
        async for session in get_db_session():
            user = User(
                id="test-rollback-user",
                email="rollback@example.com",
                hashed_password="pw",
                role="viewer",
            )
            session.add(user)
            raise RuntimeError("Intentional error to trigger rollback")
    except RuntimeError:
        pass

    async for session in get_db_session():
        result = await session.execute(text("SELECT email FROM users WHERE id = 'test-rollback-user'"))
        row = result.fetchone()
        assert row is None
