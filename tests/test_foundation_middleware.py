"""Tests for RequestID, HTTP logging, and SecurityHeaders middlewares."""

import pytest
from httpx import ASGITransport, AsyncClient
from adpilot.api.main import app


@pytest.mark.anyio
async def test_request_id_generated_and_returned():
    """Verify X-Request-ID is automatically generated and returned in headers."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/healthz")
        assert response.status_code == 200
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0


@pytest.mark.anyio
async def test_request_id_propagated_from_incoming_header():
    """Verify incoming X-Request-ID header is preserved and returned."""
    custom_id = "custom-trace-uuid-12345"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/healthz", headers={"X-Request-ID": custom_id})
        assert response.status_code == 200
        assert response.headers["X-Request-ID"] == custom_id


@pytest.mark.anyio
async def test_security_headers_present():
    """Verify all standard security headers are applied to HTTP responses."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/healthz")
        assert response.headers.get("Strict-Transport-Security") == "max-age=31536000; includeSubDomains"
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert "X-Response-Time" in response.headers
