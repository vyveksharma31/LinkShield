"""Security threat heuristics engine.

Evaluates static indicators, brand impersonation, protocol anomalies,
obfuscation patterns, and structural properties against defensive security rules.
"""
from dataclasses import dataclass
from typing import List, Tuple
from backend.app.schemas.response import (
    HeuristicFlag,
    PositiveFlag,
    SeverityEnum,
    FeatureMetrics,
)
from backend.app.engine.parser import ParsedURL

# Known high-abuse free or disposable TLDs frequently weaponized in phishing
SUSPICIOUS_TLDS = {
    "tk",
    "ml",
    "ga",
    "cf",
    "gq",
    "top",
    "xyz",
    "work",
    "click",
    "buzz",
    "loan",
    "fit",
    "rest",
    "surf",
    "country",
    "gdn",
    "mom",
}

# Verified global root authority domains for positive reputation evaluation
TRUSTED_AUTHORITIES = {
    "google.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "github.com",
    "wikipedia.org",
    "cloudflare.com",
    "mozilla.org",
    "stackoverflow.com",
}


@dataclass
class HeuristicEvaluationResult:
    """Aggregate evaluation output from security heuristics engine."""

    heuristic_flags: List[HeuristicFlag]
    positive_flags: List[PositiveFlag]
    total_penalty: int
    has_critical_flag: bool
    is_whitelisted_authority: bool


def evaluate_heuristics(
    parsed: ParsedURL,
    features: FeatureMetrics,
) -> HeuristicEvaluationResult:
    """Evaluate full suite of security threat heuristics and positive hygiene factors."""
    flags: List[HeuristicFlag] = []
    positives: List[PositiveFlag] = []
    penalty_sum = 0
    has_critical = False

    # 1. IP Host Detection (CRITICAL: +40)
    if features.is_ip_address:
        flags.append(
            HeuristicFlag(
                code="IP_HOST",
                severity=SeverityEnum.CRITICAL,
                category="Domain Forensics",
                title="Raw IP Address Host",
                description="Target uses an IP literal instead of a registered domain name, commonly used to bypass domain reputation systems.",
                evidence=parsed.hostname,
                score_impact=40,
            )
        )
        penalty_sum += 40
        has_critical = True

    # 2. Credential Delimiter Trick (@ Symbol) (CRITICAL: +40)
    if features.count_at > 0 or parsed.has_userinfo:
        flags.append(
            HeuristicFlag(
                code="AT_SYMBOL_OBFUSCATION",
                severity=SeverityEnum.CRITICAL,
                category="Syntax Anomaly",
                title="Credential Delimiter Abuse (@ Symbol)",
                description="URL embeds an '@' delimiter in the authority component to obscure the destination host (RFC 3986 userinfo trick).",
                evidence=f"{max(1, features.count_at)} '@' delimiter(s) detected",
                score_impact=40,
            )
        )
        penalty_sum += 40
        has_critical = True

    # 3. IDN Homoglyph Domain Spoofing (CRITICAL: +45)
    if parsed.has_homoglyphs:
        flags.append(
            HeuristicFlag(
                code="HOMOGLYPH_SPOOFING",
                severity=SeverityEnum.CRITICAL,
                category="Brand Forensics",
                title="IDN Homoglyph Domain Spoofing",
                description="Hostname employs Cyrillic, Greek, or visual lookalike Unicode characters to visually spoof a legitimate domain.",
                evidence=f"Decoded: {parsed.decoded_hostname} (Confusables: {', '.join(set(parsed.homoglyphs_detected))})",
                score_impact=45,
            )
        )
        penalty_sum += 45
        has_critical = True

    # 4. Brand Impersonation (CRITICAL: +45)
    if features.has_brand_in_subdomain or features.has_brand_in_path:
        location = "subdomain" if features.has_brand_in_subdomain else "path/query"
        flags.append(
            HeuristicFlag(
                code="BRAND_IMPERSONATION",
                severity=SeverityEnum.CRITICAL,
                category="Brand Forensics",
                title="Brand Impersonation Detected",
                description=f"A high-value brand token was identified in the {location}, but the registered domain does not belong to that organization.",
                evidence=f"Target token mimicked on {parsed.registered_domain}",
                score_impact=45,
            )
        )
        penalty_sum += 45
        has_critical = True

    # 5. Excessive Subdomain Depth (HIGH: +25)
    if features.subdomain_depth >= 3:
        flags.append(
            HeuristicFlag(
                code="EXCESSIVE_SUBDOMAINS",
                severity=SeverityEnum.HIGH,
                category="Structural Anomaly",
                title="Excessive Subdomain Nesting",
                description="Unusually deep subdomain hierarchy (>= 3 levels) commonly employed to conceal true hosting infrastructure.",
                evidence=f"{features.subdomain_depth} levels ({parsed.subdomain})",
                score_impact=25,
            )
        )
        penalty_sum += 25

    # 6. Suspicious TLD Lookup (HIGH: +20)
    clean_suffix = parsed.suffix.lower()
    if clean_suffix in SUSPICIOUS_TLDS:
        flags.append(
            HeuristicFlag(
                code="SUSPICIOUS_TLD",
                severity=SeverityEnum.HIGH,
                category="Domain Forensics",
                title="High-Risk Top-Level Domain",
                description=f"TLD '.{clean_suffix}' is frequently associated with disposable, low-reputation malicious infrastructure.",
                evidence=f".{clean_suffix}",
                score_impact=20,
            )
        )
        penalty_sum += 20

    # 7. Hex Encoded Obfuscation (MEDIUM: +15)
    has_evasive_hex = "%2e" in parsed.original_url.lower() or "%2f" in parsed.original_url.lower()
    if features.count_percent >= 3 or (features.has_hex_encoded_char and has_evasive_hex):
        flags.append(
            HeuristicFlag(
                code="HEX_ENCODED_OBFUSCATION",
                severity=SeverityEnum.MEDIUM,
                category="Syntax Anomaly",
                title="Obfuscated Hex Character Encoding",
                description="URL contains excessive or evasive percent-encoded hexadecimal escapes designed to bypass security filters.",
                evidence=f"{features.count_percent} '%' escape sequences",
                score_impact=15,
            )
        )
        penalty_sum += 15

    # 8. Authentication Lure Keywords (MEDIUM: +15)
    if features.count_suspicious_keywords >= 2:
        flags.append(
            HeuristicFlag(
                code="AUTH_KEYWORD_PATH",
                severity=SeverityEnum.MEDIUM,
                category="Lexical Anomaly",
                title="Authentication Lure Keywords",
                description="Path or query string contains multiple sensitive credentials and authentication tokens.",
                evidence=f"{features.count_suspicious_keywords} lure keywords",
                score_impact=15,
            )
        )
        penalty_sum += 15

    # 9. High Hostname Entropy / Potential DGA (MEDIUM: +15)
    if features.entropy_hostname > 3.8 and len(parsed.hostname) >= 10 and not features.is_ip_address:
        flags.append(
            HeuristicFlag(
                code="HIGH_HOST_ENTROPY",
                severity=SeverityEnum.MEDIUM,
                category="Algorithmic Anomaly",
                title="High Hostname Entropy (Potential DGA)",
                description="Hostname randomness exceeds 3.8 bits, indicating potential domain generation algorithm (DGA) or randomized beacon host.",
                evidence=f"{features.entropy_hostname} bits/symbol",
                score_impact=15,
            )
        )
        penalty_sum += 15

    # 10. URL Shortener Service (MEDIUM: +15)
    if features.is_shortened_url:
        flags.append(
            HeuristicFlag(
                code="URL_SHORTENER",
                severity=SeverityEnum.MEDIUM,
                category="Domain Forensics",
                title="URL Shortener Service",
                description="Public link redirection service obscures final destination, preventing direct inspection.",
                evidence=parsed.registered_domain,
                score_impact=15,
            )
        )
        penalty_sum += 15

    # 11. Non-Standard Port (LOW: +10)
    if features.has_non_standard_port:
        flags.append(
            HeuristicFlag(
                code="NON_STANDARD_PORT",
                severity=SeverityEnum.LOW,
                category="Network Hygiene",
                title="Non-Standard Service Port",
                description="URL targets a non-standard port instead of standard HTTP (80) or HTTPS (443).",
                evidence=f":{parsed.port}",
                score_impact=10,
            )
        )
        penalty_sum += 10

    # Positive Hygiene Factors
    if features.is_https:
        positives.append(
            PositiveFlag(
                category="Transport Security",
                title="Valid HTTPS Transport",
                description="Communication is encrypted using TLS protocol (port 443).",
            )
        )

    if not features.has_non_standard_port:
        positives.append(
            PositiveFlag(
                category="Network Hygiene",
                title="Standard Web Port",
                description="Target communicates over standard HTTP/HTTPS ports.",
            )
        )

    if features.subdomain_depth <= 1 and not features.is_ip_address:
        positives.append(
            PositiveFlag(
                category="Domain Structure",
                title="Clean Domain Hierarchy",
                description="Standard domain and subdomain structure without excessive nesting.",
            )
        )

    is_whitelisted = (
        parsed.registered_domain in TRUSTED_AUTHORITIES
        and features.count_suspicious_keywords == 0
        and not features.has_brand_in_subdomain
        and not features.has_brand_in_path
    )

    if is_whitelisted:
        positives.append(
            PositiveFlag(
                category="Reputation",
                title="Verified Global Authority",
                description=f"Domain '{parsed.registered_domain}' belongs to a top verified root authority with clean path indicators.",
            )
        )

    return HeuristicEvaluationResult(
        heuristic_flags=flags,
        positive_flags=positives,
        total_penalty=penalty_sum,
        has_critical_flag=has_critical,
        is_whitelisted_authority=is_whitelisted,
    )
