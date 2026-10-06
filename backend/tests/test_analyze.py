"""Tests for /api/v1/analyze endpoint and input validation."""
import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.main import app


@pytest.mark.anyio
async def test_analyze_valid_legitimate_url():
    """Verify that a standard legitimate URL returns 200 with full analysis response."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "https://example.com/about"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "https://example.com/about"
        assert data["verdict"] == "LEGITIMATE"
        assert data["risk_score"] < 25
        assert "features" in data
        assert data["features"]["is_https"] is True
        assert len(data["positive_flags"]) > 0
        assert "recommendations" in data


@pytest.mark.anyio
async def test_analyze_suspicious_ip_url():
    """Verify that an IP-based URL triggers threat flags and higher risk score."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "http://192.168.1.100/login/verify"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["verdict"] in ("SUSPICIOUS", "PHISHING")
        assert data["risk_score"] >= 40
        assert data["features"]["is_ip_address"] is True
        flags = [f["code"] for f in data["heuristic_flags"]]
        assert "IP_HOST" in flags


@pytest.mark.anyio
async def test_analyze_rejects_empty_url():
    """Verify that an empty or whitespace-only URL returns 422 Unprocessable Entity."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "   "},
        )
        assert response.status_code == 422


@pytest.mark.anyio
async def test_analyze_rejects_dangerous_scheme():
    """Verify that non-web dangerous schemes like javascript: are rejected with 422."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "javascript:alert(1)"},
        )
        assert response.status_code == 422
