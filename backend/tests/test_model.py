"""Unit tests for the machine learning model loader and inference engine."""
import pytest
from backend.app.ml.model_loader import get_model_loader, ModelLoader
from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features
from backend.app.schemas.response import MlPrediction


def test_model_loader_initialization():
    """Verify ModelLoader loads serialized Random Forest model successfully."""
    loader = get_model_loader()
    assert loader is not None
    assert loader.is_loaded is True
    assert loader.model is not None
    assert "accuracy" in loader.metadata.get("metrics", {})


def test_ml_prediction_legitimate_url():
    """Verify ML model produces low phishing probability for standard legitimate URL."""
    loader = get_model_loader()
    parsed = normalize_and_parse_url("https://www.google.com/search?q=cybersecurity")
    features = extract_features(parsed)

    prediction = loader.predict(features)
    assert isinstance(prediction, MlPrediction)
    assert prediction.raw_label == "legitimate"
    assert prediction.phishing_probability < 0.50
    assert 0.50 <= prediction.confidence <= 1.0
    assert prediction.model_version == "rf-v1.0"


def test_ml_prediction_phishing_url():
    """Verify ML model produces high phishing probability for deceptive URL."""
    loader = get_model_loader()
    parsed = normalize_and_parse_url("https://paypal.secure-verification-portal.com/login")
    features = extract_features(parsed)

    prediction = loader.predict(features)
    assert isinstance(prediction, MlPrediction)
    assert prediction.raw_label == "phishing"
    assert prediction.phishing_probability > 0.70
    assert 0.50 <= prediction.confidence <= 1.0


def test_failsoft_fallback_when_model_unloaded(monkeypatch):
    """Verify graceful fail-soft fallback returns reasonable baseline without crashing."""
    mock_loader = ModelLoader.__new__(ModelLoader)
    mock_loader.model = None
    mock_loader.metadata = {}
    mock_loader.is_loaded = False

    parsed = normalize_and_parse_url("http://192.168.1.1/login")
    features = extract_features(parsed)

    pred = mock_loader.predict(features)
    assert isinstance(pred, MlPrediction)
    assert pred.model_version == "heuristic-failsoft-v1.0"
    assert pred.phishing_probability > 0.40
