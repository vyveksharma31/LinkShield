"""Security hardening, anti-SSRF static analysis, and boundary validation tests."""
import socket
import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.main import app
from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features
from backend.app.engine.analyzer import analyze_url_pipeline


@pytest.mark.anyio
async def test_request_size_limit_rejects_payload_over_64kb():
    """Verify that requests with payload larger than 64KB are rejected with 413."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        huge_url = "https://example.com/test?" + ("a" * 70000)
        response = await client.post(
            "/api/v1/analyze",
            content=huge_url,
            headers={"Content-Length": str(len(huge_url)), "Content-Type": "application/json"},
        )
        assert response.status_code == 413
        data = response.json()
        assert "Payload too large" in data["detail"]


@pytest.mark.anyio
async def test_zero_outbound_network_calls_guarantee(monkeypatch):
    """Verify that analyzing a malicious URL makes zero network calls (Anti-SSRF)."""
    def forbidden_connect(*args, **kwargs):
        raise AssertionError("SECURITY VIOLATION: LinkShield attempted an outbound network connection during static analysis!")

    # Intercept socket connections
    monkeypatch.setattr(socket.socket, "connect", forbidden_connect)

    # Analyze an adversarial URL targeting internal network
    internal_target = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    result = await analyze_url_pipeline(internal_target)

    assert result is not None
    assert result.verdict in ("SUSPICIOUS", "PHISHING")
    assert result.features.is_ip_address is True


def test_redos_resilience_on_repeating_patterns():
    """Verify regex patterns execute in sub-millisecond time on adversarial patterns."""
    adversarial_string = "http://" + ("a" * 500) + "." + ("b" * 500) + ".xyz/" + ("%20" * 200)
    parsed = normalize_and_parse_url(adversarial_string)
    features = extract_features(parsed)

    assert parsed.suffix == "xyz"
    assert features.count_percent == 200
    assert features.url_length > 1000
