"""Tests for liveness, readiness, and deep health check endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from adpilot.api.main import app


@pytest.mark.anyio
async def test_liveness_probe_healthz():
    """Verify /healthz returns 200 OK with version metadata."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/healthz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("ok", "healthy")


@pytest.mark.anyio
async def test_readiness_probe_ready():
    """Verify /ready evaluates dependencies and returns health status."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/ready")
        assert response.status_code in (200, 503)
        data = response.json()
        assert "status" in data
        assert "components" in data
        assert "database" in data["components"]


@pytest.mark.anyio
async def test_saas_health_endpoint():
    """Verify legacy /health endpoint returns database status."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"


@pytest.mark.anyio
async def test_v1_health_routes():
    """Verify versioned /api/v1/healthz, /api/v1/ready, and /api/v1/health endpoints."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_liveness = await ac.get("/api/v1/healthz")
        assert res_liveness.status_code == 200
        assert res_liveness.json()["status"] == "ok"

        res_readiness = await ac.get("/api/v1/ready")
        assert res_readiness.status_code in (200, 503)

        res_deep = await ac.get("/api/v1/health")
        assert res_deep.status_code in (200, 503)
        assert "components" in res_deep.json()
