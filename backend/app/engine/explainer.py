"""Explainability and security recommendation generator for LinkShield.

Translates technical indicators, mathematical metrics, and classification verdicts
into structured, context-aware operational guidance for security analysts and end-users.
"""
from typing import List
from backend.app.schemas.response import VerdictEnum, HeuristicFlag, PositiveFlag, FeatureMetrics
from backend.app.engine.parser import ParsedURL


def generate_recommendations(
    verdict: VerdictEnum,
    risk_score: int,
    heuristic_flags: List[HeuristicFlag],
    positive_flags: List[PositiveFlag],
    parsed: ParsedURL,
    features: FeatureMetrics,
) -> List[str]:
    """Generate context-specific security guidance grounded in detected forensic evidence."""
    recs: List[str] = []

    # 1. Primary Verdict Guidance
    if verdict == VerdictEnum.PHISHING:
        recs.append("DO NOT visit this destination, submit credentials, or approve multi-factor authorization prompts.")
    elif verdict == VerdictEnum.SUSPICIOUS:
        recs.append("Exercise extreme caution before navigating to this link; structural and lexical anomalies were identified.")
    else:
        recs.append("URL exhibits standard structural hygiene with verified legitimate indicators.")

    # 2. Indicator-Specific Actionable Recommendations
    flag_codes = {f.code for f in heuristic_flags}

    if "HOMOGLYPH_SPOOFING" in flag_codes:
        recs.append(
            f"Visual spoofing detected: Domain uses lookalike Internationalized Domain Name characters mimicking legitimate text ({parsed.decoded_hostname})."
        )

    if "BRAND_IMPERSONATION" in flag_codes:
        recs.append(
            f"Brand spoofing detected: High-value enterprise brand tokens appear outside the authentic registered domain ({parsed.registered_domain})."
        )

    if "IP_HOST" in flag_codes:
        recs.append(
            "Host targets a raw numerical IP address rather than a registered domain name, circumventing standard DNS reputation controls."
        )

    if "AT_SYMBOL_OBFUSCATION" in flag_codes:
        recs.append(
            "Authority manipulation detected: URL exploits '@' userinfo delimiter syntax to mask the true destination host."
        )

    if "SUSPICIOUS_TLD" in flag_codes:
        recs.append(
            f"Domain uses high-abuse top-level domain '.{parsed.suffix}', frequently observed in short-lived phishing campaigns."
        )

    if "URL_SHORTENER" in flag_codes:
        recs.append(
            "Target uses a URL shortening redirection service that conceals the ultimate target host."
        )

    if "HEX_ENCODED_OBFUSCATION" in flag_codes:
        recs.append(
            "Excessive hexadecimal escape encodings detected, indicative of signature-evasion techniques."
        )

    if "AUTH_KEYWORD_PATH" in flag_codes:
        recs.append(
            "Target path contains authentication keywords while hosted on an unverified domain."
        )

    # 3. Closing Remediation Advice
    if verdict == VerdictEnum.PHISHING:
        recs.append("Submit this URL to your security operations team (SOC) and consider blocking domain at network boundaries.")
    elif verdict == VerdictEnum.SUSPICIOUS:
        recs.append("Verify destination address directly with the purported organization via an independent official channel.")
    else:
        recs.append("Continue to adhere to standard organizational security practices when interacting with external resources.")

    return recs
