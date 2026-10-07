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
        assert data["risk_score"] <= 25
        assert "features" in data
        assert data["features"]["is_https"] is True
        assert len(data["positive_flags"]) > 0
        assert "recommendations" in data
        assert data["ml_prediction"] is not None


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
        assert data["risk_score"] >= 60
        assert data["features"]["is_ip_address"] is True
        flags = [f["code"] for f in data["heuristic_flags"]]
        assert "IP_HOST" in flags


@pytest.mark.anyio
async def test_analyze_brand_impersonation_url():
    """Verify that spoofed brand subdomain triggers critical override and PHISHING verdict."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "https://paypal.secure-verification-portal.com/login"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["verdict"] == "PHISHING"
        assert data["risk_score"] >= 75
        flags = [f["code"] for f in data["heuristic_flags"]]
        assert "BRAND_IMPERSONATION" in flags


@pytest.mark.anyio
async def test_analyze_idn_homoglyph_url():
    """Verify that an IDN punycode homoglyph triggers PHISHING verdict and spoof flag."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "https://xn--pypal-4ve.com/signin"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["verdict"] == "PHISHING"
        assert data["risk_score"] >= 75
        flags = [f["code"] for f in data["heuristic_flags"]]
        assert "HOMOGLYPH_SPOOFING" in flags


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


@pytest.mark.anyio
async def test_analyze_rejects_oversized_url():
    """Verify that URLs exceeding 2048 characters are rejected with 422."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "https://example.com/" + "a" * 2050},
        )
        assert response.status_code == 422


@pytest.mark.anyio
async def test_analyze_rejects_null_bytes():
    """Verify that URLs with null byte injection are rejected with 422."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": "https://example.com/login\x00evil"},
        )
        assert response.status_code == 422
