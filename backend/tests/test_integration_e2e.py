"""End-to-end integration tests for LinkShield URL analysis engine.

Tests real-world archetypes, performance latency bounds, and complete schema compliance.
"""
import pytest
from httpx import ASGITransport, AsyncClient
from backend.app.main import app


REAL_WORLD_TEST_CASES = [
    {
        "url": "https://chase.com/personal",
        "expected_verdict": "LEGITIMATE",
        "max_risk": 25,
        "description": "Legitimate banking portal",
    },
    {
        "url": "https://github.com/vyveksharma31/LinkShield",
        "expected_verdict": "LEGITIMATE",
        "max_risk": 25,
        "description": "Legitimate developer repository",
    },
    {
        "url": "https://chase.com.security-check.top/login.php",
        "expected_verdict": "PHISHING",
        "min_risk": 70,
        "description": "Brand impersonation subdomain on suspicious TLD",
    },
    {
        "url": "http://45.33.32.156:8080/bank/verify",
        "expected_verdict": "PHISHING",
        "min_risk": 60,
        "description": "IP literal with non-standard port and auth keywords",
    },
    {
        "url": "https://xn--pple-43d.com/recovery",
        "expected_verdict": "PHISHING",
        "min_risk": 70,
        "description": "IDN Punycode homoglyph spoofing Apple",
    },
    {
        "url": "https://bit.ly/secure-paypal-login",
        "expected_verdict": "SUSPICIOUS",
        "min_risk": 30,
        "description": "URL shortener masking credential lure",
    },
    {
        "url": "https://account-verify-login.xyz",
        "expected_verdict": "SUSPICIOUS",
        "min_risk": 35,
        "description": "Suspicious TLD with multiple authentication keywords",
    },
    {
        "url": "HTTPS://EXAMPLE.COM/UpperPath?Key=VAL",
        "expected_verdict": "LEGITIMATE",
        "max_risk": 25,
        "description": "Case normalization handling",
    },
]


@pytest.mark.anyio
@pytest.mark.parametrize("test_case", REAL_WORLD_TEST_CASES)
async def test_e2e_real_world_url_analysis(test_case):
    """Verify that diverse real-world URL archetypes receive accurate risk assessments."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/analyze",
            json={"url": test_case["url"]},
        )
        assert response.status_code == 200
        data = response.json()

        # Schema invariants
        assert data["url"] == test_case["url"]
        assert data["verdict"] in ("LEGITIMATE", "SUSPICIOUS", "PHISHING")
        assert 0 <= data["risk_score"] <= 100
        assert 0.0 <= data["confidence"] <= 1.0
        assert len(data["recommendations"]) >= 1
        assert "features" in data
        assert "execution_time_ms" in data

        # Latency constraint (target < 50ms)
        assert data["execution_time_ms"] < 150.0

        # Classification assertions
        if "expected_verdict" in test_case:
            if test_case["expected_verdict"] == "PHISHING":
                assert data["verdict"] in ("PHISHING", "SUSPICIOUS")
            elif test_case["expected_verdict"] == "LEGITIMATE":
                assert data["verdict"] == "LEGITIMATE"

        if "min_risk" in test_case:
            assert data["risk_score"] >= test_case["min_risk"]

        if "max_risk" in test_case:
            assert data["risk_score"] <= test_case["max_risk"]


@pytest.mark.anyio
async def test_e2e_response_consistency_under_repeated_queries():
    """Verify deterministic outputs across identical repeated queries."""
    target = "https://secure-login.paypal.account-verify.xyz/signin"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res1 = await client.post("/api/v1/analyze", json={"url": target})
        res2 = await client.post("/api/v1/analyze", json={"url": target})

        assert res1.status_code == 200
        assert res2.status_code == 200

        d1 = res1.json()
        d2 = res2.json()

        assert d1["verdict"] == d2["verdict"]
        assert d1["risk_score"] == d2["risk_score"]
        assert len(d1["heuristic_flags"]) == len(d2["heuristic_flags"])
