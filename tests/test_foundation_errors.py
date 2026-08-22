"""Tests for centralized RFC 7807 Problem Details error handling."""

import pytest
from httpx import ASGITransport, AsyncClient
from adpilot.api.main import app


@pytest.mark.anyio
async def test_rfc7807_validation_error():
    """Verify schema validation error returns 422 with RFC 7807 Problem Details format."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Send empty/invalid payload to endpoint requiring CampaignInput
        response = await ac.post("/api/campaigns/run", json={"invalid_field": 123})
        assert response.status_code == 422

        data = response.json()
        assert data["status"] == 422
        assert "Validation Error" in data["title"]
        assert "invalid_params" in data
        assert "timestamp" in data
        assert "instance" in data
        assert "type" in data


@pytest.mark.anyio
async def test_rfc7807_not_found_error():
    """Verify 404 resource request returns RFC 7807 Problem Details format."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/campaigns/non-existent-campaign-id-999")
        assert response.status_code == 404

        data = response.json()
        assert data["status"] == 404
        assert "detail" in data
        assert "instance" in data
        assert "timestamp" in data


@pytest.mark.anyio
async def test_rfc7807_unauthorized_error():
    """Verify 401 unauthenticated request returns RFC 7807 Problem Details."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/audit-logs")
        assert response.status_code == 401

        data = response.json()
        assert data["status"] == 401
        assert "title" in data
        assert "timestamp" in data
