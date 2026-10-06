"""Tests for root and health diagnostics endpoints."""
import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.main import app


@pytest.mark.anyio
async def test_root_endpoint():
    """Verify that the root endpoint returns service metadata."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "LinkShield"
        assert data["status"] == "online"
        assert "version" in data
        assert "documentation" in data


@pytest.mark.anyio
async def test_health_endpoint():
    """Verify that the /api/v1/health endpoint returns health status."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data
        assert isinstance(data["model_loaded"], bool)
