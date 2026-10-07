"""Lightweight ML inference loader and predictor for LinkShield.

Loads serialized Random Forest model artifact and computes calibrated
phishing probability and confidence metrics. Implements graceful fail-soft
fallback if model artifacts are unavailable.
"""
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import joblib
import numpy as np

from backend.app.schemas.response import FeatureMetrics, MlPrediction
from backend.app.engine.features import features_to_vector

logger = logging.getLogger("linkshield.ml")

MODEL_FILENAME = "phishing_rf_v1.joblib"


class ModelLoader:
    """Manages loading, caching, and inference for the LinkShield ML classifier."""

    _instance: Optional["ModelLoader"] = None

    def __init__(self) -> None:
        self.model: Optional[Any] = None
        self.metadata: Dict[str, Any] = {}
        self.is_loaded: bool = False
        self._initialize_model()

    @classmethod
    def get_instance(cls) -> "ModelLoader":
        """Get or initialize singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _locate_model_file(self) -> Optional[Path]:
        """Locate the serialized model artifact across common execution roots."""
        current_dir = Path(__file__).resolve().parent
        candidate_paths = [
            current_dir.parent.parent / "models" / MODEL_FILENAME,
            current_dir.parent.parent / "backend" / "models" / MODEL_FILENAME,
            Path.cwd() / "backend" / "models" / MODEL_FILENAME,
            Path.cwd() / "models" / MODEL_FILENAME,
        ]

        for p in candidate_paths:
            if p.exists() and p.is_file():
                return p
        return None

    def _initialize_model(self) -> None:
        """Attempt to deserialize and load the trained model into memory."""
        model_path = self._locate_model_file()
        if not model_path:
            logger.warning("LinkShield ML model artifact '%s' not found. Operating in heuristic fail-soft mode.", MODEL_FILENAME)
            self.is_loaded = False
            return

        try:
            import pickle
            try:
                with open(model_path, "rb") as f:
                    bundle = pickle.load(f)
            except Exception:
                bundle = joblib.load(model_path)

            self.model = bundle["model"]
            self.metadata = bundle.get("metadata", {})
            self.is_loaded = True
            logger.info("Successfully initialized LinkShield ML model: %s (%s)", self.metadata.get("model_version", "v1.0"), model_path)
        except Exception as e:
            logger.error("Failed to load ML model artifact from %s: %s", model_path, e)
            self.is_loaded = False

    def predict(self, features: FeatureMetrics) -> MlPrediction:
        """Execute inference on extracted features and return MlPrediction."""
        if self.is_loaded and self.model is not None:
            try:
                vector = features_to_vector(features)
                X = np.array([vector], dtype=np.float32)
                probabilities = self.model.predict_proba(X)[0]
                phishing_prob = float(probabilities[1])

                raw_label = "phishing" if phishing_prob >= 0.50 else "legitimate"
                # Calibrate confidence based on distance from decision threshold (0.50)
                distance = abs(phishing_prob - 0.50) * 2.0
                confidence = round(0.70 + (distance * 0.28), 4)

                return MlPrediction(
                    phishing_probability=round(phishing_prob, 4),
                    raw_label=raw_label,
                    model_version=self.metadata.get("model_version", "rf-v1.0"),
                    confidence=confidence,
                )
            except Exception as e:
                logger.error("Inference exception encountered: %s. Falling back to heuristic baseline.", e)

        # Graceful Fail-Soft Baseline
        base_score = 0.05
        if features.is_ip_address:
            base_score += 0.40
        if features.count_at > 0:
            base_score += 0.35
        if features.has_brand_in_subdomain:
            base_score += 0.35
        if features.subdomain_depth >= 3:
            base_score += 0.20
        if features.is_shortened_url:
            base_score += 0.15
        if features.count_suspicious_keywords >= 2:
            base_score += 0.15

        phishing_prob = min(0.99, max(0.01, round(base_score, 4)))
        return MlPrediction(
            phishing_probability=phishing_prob,
            raw_label="phishing" if phishing_prob >= 0.50 else "legitimate",
            model_version="heuristic-failsoft-v1.0",
            confidence=0.75,
        )


def get_model_loader() -> ModelLoader:
    """Return the global ModelLoader singleton."""
    return ModelLoader.get_instance()
