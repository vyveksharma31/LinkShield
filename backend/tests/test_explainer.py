"""Unit tests for the explainability and recommendation engine."""
import pytest
from backend.app.schemas.response import VerdictEnum, HeuristicFlag, PositiveFlag, SeverityEnum
from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features
from backend.app.engine.explainer import generate_recommendations


def test_phishing_recommendations_content():
    """Verify phishing recommendations include stern warning and forensic notes."""
    parsed = normalize_and_parse_url("https://paypal.verification-center.com/login")
    features = extract_features(parsed)
    flag = HeuristicFlag(
        code="BRAND_IMPERSONATION",
        severity=SeverityEnum.CRITICAL,
        category="Brand Forensics",
        title="Brand Impersonation Detected",
        description="PayPal mimicked",
        evidence="paypal in subdomain",
        score_impact=45,
    )

    recs = generate_recommendations(
        verdict=VerdictEnum.PHISHING,
        risk_score=85,
        heuristic_flags=[flag],
        positive_flags=[],
        parsed=parsed,
        features=features,
    )

    assert len(recs) >= 3
    assert any("DO NOT" in r for r in recs)
    assert any("Brand spoofing detected" in r for r in recs)


def test_legitimate_recommendations_content():
    """Verify legitimate recommendations are calm and informative."""
    parsed = normalize_and_parse_url("https://github.com/vyveksharma31/LinkShield")
    features = extract_features(parsed)

    recs = generate_recommendations(
        verdict=VerdictEnum.LEGITIMATE,
        risk_score=5,
        heuristic_flags=[],
        positive_flags=[],
        parsed=parsed,
        features=features,
    )

    assert len(recs) >= 2
    assert any("standard structural hygiene" in r for r in recs)
