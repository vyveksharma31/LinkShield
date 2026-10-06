"""Pydantic schemas for structured API responses."""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class VerdictEnum(str, Enum):
    LEGITIMATE = "LEGITIMATE"
    SUSPICIOUS = "SUSPICIOUS"
    PHISHING = "PHISHING"


class SeverityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class HeuristicFlag(BaseModel):
    """Specific threat indicator discovered during analysis."""

    code: str = Field(..., description="Unique machine-readable indicator identifier")
    severity: SeverityEnum = Field(..., description="Threat severity tier")
    category: str = Field(..., description="Forensic category (e.g. Domain Forensics, Lexical Anomaly)")
    title: str = Field(..., description="Concise human-readable finding title")
    description: str = Field(..., description="Detailed technical reason for this finding")
    evidence: str = Field(..., description="Concrete data or substring that triggered the indicator")
    score_impact: int = Field(..., description="Points added to the composite risk score")


class PositiveFlag(BaseModel):
    """Positive hygiene indicator that reduces risk or indicates legitimacy."""

    category: str = Field(..., description="Security category (e.g. Transport, Reputation)")
    title: str = Field(..., description="Positive indicator title")
    description: str = Field(..., description="Detailed reason why this factor reduces suspicion")


class MlPrediction(BaseModel):
    """Machine learning inference details."""

    phishing_probability: float = Field(..., ge=0.0, le=1.0, description="Calibrated model probability of phishing")
    raw_label: str = Field(..., description="Raw model classification (phishing | legitimate)")
    model_version: str = Field(..., description="Identifier and version of the serialized ML model")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Statistical model confidence")


class FeatureMetrics(BaseModel):
    """Extracted URL features for forensic inspection."""

    url_length: int
    hostname_length: int
    path_length: int
    query_length: int
    num_path_segments: int
    num_query_params: int
    tld_length: int
    subdomain_depth: int
    count_dots: int
    count_hyphens: int
    count_underscores: int
    count_slashes: int
    count_question: int
    count_equals: int
    count_at: int
    count_percent: int
    count_digits: int
    digit_ratio: float
    entropy_url: float
    entropy_hostname: float
    entropy_path: float
    count_suspicious_keywords: int
    has_brand_in_subdomain: bool
    has_brand_in_path: bool
    is_shortened_url: bool
    has_hex_encoded_char: bool
    is_ip_address: bool
    is_https: bool
    has_non_standard_port: bool
    is_punycode: bool
    tld: str
    domain: str


class AnalysisResponse(BaseModel):
    """Complete security assessment report for an analyzed URL."""

    url: str = Field(..., description="Original requested URL")
    normalized_url: str = Field(..., description="Sanitized and normalized URL string")
    verdict: VerdictEnum = Field(..., description="Final security classification")
    risk_score: int = Field(..., ge=0, le=100, description="Composite threat score from 0 (Safe) to 100 (Critical)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence in the final security assessment")
    ml_prediction: Optional[MlPrediction] = Field(None, description="ML inference details if available")
    heuristic_flags: List[HeuristicFlag] = Field(default_factory=list, description="Threat indicators detected")
    positive_flags: List[PositiveFlag] = Field(default_factory=list, description="Positive security hygiene factors")
    features: FeatureMetrics = Field(..., description="Detailed metrics extracted from the URL")
    recommendations: List[str] = Field(default_factory=list, description="Actionable security guidance")
    analyzed_at: str = Field(..., description="ISO-8601 UTC timestamp of analysis")
    execution_time_ms: float = Field(..., description="End-to-end analysis latency in milliseconds")


class HealthResponse(BaseModel):
    """System health and operational status response."""

    status: str = Field(default="healthy", description="Operational status of backend service")
    version: str = Field(..., description="LinkShield API version")
    model_loaded: bool = Field(..., description="Whether the ML model is initialized in memory")
    timestamp: str = Field(..., description="Current ISO-8601 server timestamp")
