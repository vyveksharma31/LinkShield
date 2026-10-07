"""Unit tests for the hybrid risk scoring engine and safety overrides."""
import pytest
from backend.app.schemas.response import VerdictEnum, MlPrediction, SeverityEnum, HeuristicFlag
from backend.app.engine.heuristics import HeuristicEvaluationResult
from backend.app.engine.risk_scorer import calculate_composite_risk


def test_clean_legitimate_scoring():
    """Verify clean URL with 0 heuristics and low ML probability yields LEGITIMATE verdict."""
    ml_pred = MlPrediction(
        phishing_probability=0.04,
        raw_label="legitimate",
        model_version="rf-v1.0",
        confidence=0.92,
    )
    heuristics = HeuristicEvaluationResult(
        heuristic_flags=[],
        positive_flags=[],
        total_penalty=0,
        has_critical_flag=False,
        is_whitelisted_authority=True,
    )

    result = calculate_composite_risk(ml_pred, heuristics)
    assert result.verdict == VerdictEnum.LEGITIMATE
    assert result.risk_score <= 10
    assert result.confidence >= 0.90


def test_critical_override_forces_phishing():
    """Verify that a CRITICAL heuristic forces risk score to at least 75 (PHISHING)."""
    # Even if ML probability was low (0.10)
    ml_pred = MlPrediction(
        phishing_probability=0.10,
        raw_label="legitimate",
        model_version="rf-v1.0",
        confidence=0.80,
    )
    crit_flag = HeuristicFlag(
        code="IP_HOST",
        severity=SeverityEnum.CRITICAL,
        category="Domain Forensics",
        title="Raw IP Address Host",
        description="Target uses IP literal",
        evidence="192.168.1.1",
        score_impact=40,
    )
    heuristics = HeuristicEvaluationResult(
        heuristic_flags=[crit_flag],
        positive_flags=[],
        total_penalty=40,
        has_critical_flag=True,
        is_whitelisted_authority=False,
    )

    result = calculate_composite_risk(ml_pred, heuristics)
    assert result.verdict == VerdictEnum.PHISHING
    assert result.risk_score >= 75
    assert result.override_applied is True


def test_whitelisted_authority_dampener():
    """Verify that verified root authority is dampened to at most 10 when clean."""
    ml_pred = MlPrediction(
        phishing_probability=0.20,
        raw_label="legitimate",
        model_version="rf-v1.0",
        confidence=0.85,
    )
    heuristics = HeuristicEvaluationResult(
        heuristic_flags=[],
        positive_flags=[],
        total_penalty=0,
        has_critical_flag=False,
        is_whitelisted_authority=True,
    )

    result = calculate_composite_risk(ml_pred, heuristics)
    assert result.risk_score <= 10
    assert result.verdict == VerdictEnum.LEGITIMATE


def test_suspicious_verdict_tier():
    """Verify moderate anomalies produce SUSPICIOUS classification (26-60)."""
    ml_pred = MlPrediction(
        phishing_probability=0.45,
        raw_label="legitimate",
        model_version="rf-v1.0",
        confidence=0.72,
    )
    med_flag = HeuristicFlag(
        code="URL_SHORTENER",
        severity=SeverityEnum.MEDIUM,
        category="Domain Forensics",
        title="URL Shortener Service",
        description="Public shortener",
        evidence="bit.ly",
        score_impact=15,
    )
    heuristics = HeuristicEvaluationResult(
        heuristic_flags=[med_flag],
        positive_flags=[],
        total_penalty=15,
        has_critical_flag=False,
        is_whitelisted_authority=False,
    )

    result = calculate_composite_risk(ml_pred, heuristics)
    assert result.verdict == VerdictEnum.SUSPICIOUS
    assert 26 <= result.risk_score <= 60
