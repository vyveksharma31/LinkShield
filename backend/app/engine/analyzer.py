"""Coordinator for the multi-stage LinkShield URL analysis pipeline.

Coordinates safe static parsing, feature extraction, security heuristics,
machine learning inference, composite risk scoring, and explainability.
"""
import time
from datetime import datetime, timezone

from backend.app.schemas.response import AnalysisResponse
from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features
from backend.app.engine.heuristics import evaluate_heuristics
from backend.app.ml.model_loader import get_model_loader
from backend.app.engine.risk_scorer import calculate_composite_risk
from backend.app.engine.explainer import generate_recommendations


async def analyze_url_pipeline(raw_url: str) -> AnalysisResponse:
    """Execute end-to-end defensive static URL analysis pipeline."""
    start_time = time.perf_counter()

    # Stage 1: Safe Normalization & Structural Parsing
    parsed = normalize_and_parse_url(raw_url)

    # Stage 2: 30-Dimension Feature Extraction
    features = extract_features(parsed)

    # Stage 3: Security Threat Heuristics Evaluation
    heuristic_result = evaluate_heuristics(parsed, features)

    # Stage 4: Machine Learning Inference (Random Forest Classifier)
    ml_loader = get_model_loader()
    ml_prediction = ml_loader.predict(features)

    # Stage 5: Hybrid Multi-Signal Risk Scoring
    risk_result = calculate_composite_risk(ml_prediction, heuristic_result)

    # Stage 6: Grounded Explainability & Recommendations
    recommendations = generate_recommendations(
        verdict=risk_result.verdict,
        risk_score=risk_result.risk_score,
        heuristic_flags=heuristic_result.heuristic_flags,
        positive_flags=heuristic_result.positive_flags,
        parsed=parsed,
        features=features,
    )

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return AnalysisResponse(
        url=raw_url,
        normalized_url=parsed.normalized_url,
        verdict=risk_result.verdict,
        risk_score=risk_result.risk_score,
        confidence=risk_result.confidence,
        ml_prediction=ml_prediction,
        heuristic_flags=heuristic_result.heuristic_flags,
        positive_flags=heuristic_result.positive_flags,
        features=features,
        recommendations=recommendations,
        analyzed_at=datetime.now(timezone.utc).isoformat(),
        execution_time_ms=elapsed_ms,
    )
