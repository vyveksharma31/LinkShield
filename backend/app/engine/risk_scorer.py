"""Composite risk scoring and classification engine for LinkShield.

Implements the multi-signal mathematical formulation specified in BRAIN.md Section 8:
fusing calibrated machine learning probabilities and heuristic threat penalties
with safety overrides and confidence calibration.
"""
from dataclasses import dataclass
from backend.app.schemas.response import VerdictEnum, MlPrediction
from backend.app.engine.heuristics import HeuristicEvaluationResult


@dataclass
class RiskScoringResult:
    """Calculated threat assessment metrics."""

    risk_score: int
    verdict: VerdictEnum
    confidence: float
    raw_score: float
    override_applied: bool
    override_reason: str = ""


def calculate_composite_risk(
    ml_prediction: MlPrediction,
    heuristic_result: HeuristicEvaluationResult,
) -> RiskScoringResult:
    """Compute the multi-signal hybrid risk score (0-100) and classification verdict.

    Formula:
        ml_component = ML_Probability * 100
        heuristic_penalty = min(50, total_penalty) * 2
        raw_score = 0.60 * ml_component + 0.40 * heuristic_penalty

    Overrides:
        - Critical Flag Override: If any CRITICAL indicator fired, score >= 75
        - Whitelisted Dampener: If verified root authority with clean path, score <= 10
    """
    # 1. Base components
    ml_score = ml_prediction.phishing_probability * 100.0
    # Map [0, 50] heuristic penalty to [0, 100] scale
    heuristic_score = min(50.0, float(heuristic_result.total_penalty)) * 2.0

    raw_score = (0.60 * ml_score) + (0.40 * heuristic_score)
    final_score = raw_score
    override_applied = False
    override_reason = ""

    # 2. Critical Safety Override (guaranteed high floor for severe threats)
    if heuristic_result.has_critical_flag:
        if final_score < 75.0:
            final_score = 75.0
            override_applied = True
            override_reason = "Critical security heuristic triggered (floor: 75)"

    # 3. Whitelisted Authority Dampener (prevents false positives on verified root domains)
    if heuristic_result.is_whitelisted_authority and not heuristic_result.has_critical_flag:
        if final_score > 10.0:
            final_score = 10.0
            override_applied = True
            override_reason = "Verified root authority dampener applied (cap: 10)"

    # 4. Clamp to 0-100 bounds
    bounded_score = int(round(min(100.0, max(0.0, final_score))))

    # 5. Threshold-based classification verdict
    if bounded_score >= 61:
        verdict = VerdictEnum.PHISHING
    elif bounded_score >= 26:
        verdict = VerdictEnum.SUSPICIOUS
    else:
        verdict = VerdictEnum.LEGITIMATE

    # 6. Confidence Calibration
    # Blend ML model statistical confidence with signal concordance
    ml_conf = ml_prediction.confidence
    # Concordance check: do ML probability and heuristic penalty point in the same direction?
    both_high = (ml_prediction.phishing_probability >= 0.60) and (heuristic_result.total_penalty >= 20)
    both_low = (ml_prediction.phishing_probability <= 0.30) and (heuristic_result.total_penalty == 0)

    if both_high or both_low:
        calibrated_conf = min(0.98, ml_conf + 0.08)
    else:
        calibrated_conf = max(0.65, ml_conf - 0.05)

    return RiskScoringResult(
        risk_score=bounded_score,
        verdict=verdict,
        confidence=round(calibrated_conf, 2),
        raw_score=round(raw_score, 2),
        override_applied=override_applied,
        override_reason=override_reason,
    )
