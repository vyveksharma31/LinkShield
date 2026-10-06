"""Engine coordinator for URL analysis pipeline."""
import time
from datetime import datetime, timezone
from typing import List

from backend.app.schemas.response import (
    AnalysisResponse,
    VerdictEnum,
    SeverityEnum,
    HeuristicFlag,
    PositiveFlag,
    MlPrediction,
)
from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features


async def analyze_url_pipeline(raw_url: str) -> AnalysisResponse:
    """Execute end-to-end static URL analysis pipeline."""
    start_time = time.perf_counter()

    # Step 1: Safe Parsing & Normalization
    parsed = normalize_and_parse_url(raw_url)

    # Step 2: Feature Extraction
    features = extract_features(parsed)

    heuristic_flags: List[HeuristicFlag] = []
    positive_flags: List[PositiveFlag] = []
    score_accumulator = 0

    # Step 3: Heuristic Signal Checks
    if features.is_ip_address:
        heuristic_flags.append(
            HeuristicFlag(
                code="IP_HOST",
                severity=SeverityEnum.CRITICAL,
                category="Domain Forensics",
                title="Raw IP Address Used As Hostname",
                description="The URL uses a numeric IP address instead of a registered domain name, commonly used to bypass domain reputation systems.",
                evidence=parsed.hostname,
                score_impact=40,
            )
        )
        score_accumulator += 40

    if features.count_at > 0:
        heuristic_flags.append(
            HeuristicFlag(
                code="AT_SYMBOL_OBFUSCATION",
                severity=SeverityEnum.CRITICAL,
                category="Syntax Anomaly",
                title="Credential Delimiter Trick (@ Symbol)",
                description="The URL uses an '@' symbol in the authority component to obscure the destination host.",
                evidence=f"{features.count_at} '@' character(s)",
                score_impact=35,
            )
        )
        score_accumulator += 35

    if features.has_brand_in_subdomain:
        heuristic_flags.append(
            HeuristicFlag(
                code="BRAND_IN_SUBDOMAIN",
                severity=SeverityEnum.HIGH,
                category="Brand Forensics",
                title="Target Brand Mimicked In Subdomain",
                description="A high-value targeted brand name was found inside a subdomain while the registered domain belongs to an unrelated entity.",
                evidence=parsed.subdomain,
                score_impact=30,
            )
        )
        score_accumulator += 30

    if features.subdomain_depth >= 3:
        heuristic_flags.append(
            HeuristicFlag(
                code="EXCESSIVE_SUBDOMAINS",
                severity=SeverityEnum.HIGH,
                category="Structural Anomaly",
                title="Excessive Subdomain Depth",
                description="Unusually high subdomain count (>= 3) typical of multi-level evasion redirection.",
                evidence=f"{features.subdomain_depth} subdomains",
                score_impact=20,
            )
        )
        score_accumulator += 20

    if features.count_suspicious_keywords >= 2:
        heuristic_flags.append(
            HeuristicFlag(
                code="AUTH_KEYWORDS",
                severity=SeverityEnum.MEDIUM,
                category="Lexical Anomaly",
                title="Multiple Authentication Keywords Detected",
                description="Target path or query contains sensitive security lure tokens.",
                evidence=f"{features.count_suspicious_keywords} keywords found",
                score_impact=15,
            )
        )
        score_accumulator += 15

    if features.is_shortened_url:
        heuristic_flags.append(
            HeuristicFlag(
                code="URL_SHORTENER",
                severity=SeverityEnum.MEDIUM,
                category="Domain Forensics",
                title="Known URL Shortener Service",
                description="The URL uses a public redirection service that conceals the ultimate destination.",
                evidence=parsed.registered_domain,
                score_impact=15,
            )
        )
        score_accumulator += 15

    # Positive Security Flags
    if features.is_https:
        positive_flags.append(
            PositiveFlag(
                category="Transport Security",
                title="Valid HTTPS Transport",
                description="Communication is encrypted using TLS protocol (port 443).",
            )
        )

    if not features.has_non_standard_port:
        positive_flags.append(
            PositiveFlag(
                category="Network Hygiene",
                title="Standard Web Port",
                description="Target communicates over standard HTTP/HTTPS ports.",
            )
        )

    if features.subdomain_depth <= 1 and not features.is_ip_address:
        positive_flags.append(
            PositiveFlag(
                category="Domain Structure",
                title="Clean Domain Hierarchy",
                description="Standard domain and subdomain structure without excessive nesting.",
            )
        )

    # Step 4: Risk Scoring Calculation
    risk_score = min(100, max(0, score_accumulator))

    if risk_score >= 61:
        verdict = VerdictEnum.PHISHING
        confidence = 0.90
        recommendations = [
            "DO NOT visit or submit credentials on this website.",
            "Deceptive characteristics indicate active phishing or credential harvesting infrastructure.",
            "Report this URL to your security operations team.",
        ]
    elif risk_score >= 26:
        verdict = VerdictEnum.SUSPICIOUS
        confidence = 0.75
        recommendations = [
            "Exercise caution before interacting with this destination.",
            "Verify the authenticity of the domain through an independent official channel.",
            "Do not download attachments or enter passwords.",
        ]
    else:
        verdict = VerdictEnum.LEGITIMATE
        confidence = 0.88
        recommendations = [
            "URL exhibits standard structural characteristics with no obvious phishing signals.",
            "Always follow standard organizational web hygiene practices.",
        ]

    # Baseline ML prediction object
    ml_prediction = MlPrediction(
        phishing_probability=round(risk_score / 100.0, 4),
        raw_label="phishing" if risk_score >= 61 else "legitimate",
        model_version="heuristic-baseline-v1.0",
        confidence=confidence,
    )

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return AnalysisResponse(
        url=raw_url,
        normalized_url=parsed.normalized_url,
        verdict=verdict,
        risk_score=risk_score,
        confidence=confidence,
        ml_prediction=ml_prediction,
        heuristic_flags=heuristic_flags,
        positive_flags=positive_flags,
        features=features,
        recommendations=recommendations,
        analyzed_at=datetime.now(timezone.utc).isoformat(),
        execution_time_ms=elapsed_ms,
    )
