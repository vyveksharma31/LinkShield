"""Lexical, structural, and information-theoretic feature extraction engine.

Extracts 30 distinct URL characteristics statically for feeding both the
machine learning inference pipeline and the security heuristics engine.
"""
import math
import re
from collections import Counter
from typing import Dict, List, Any
from backend.app.schemas.response import FeatureMetrics
from backend.app.engine.parser import ParsedURL

# Security-critical tokens commonly weaponized in phishing lure paths/queries
SUSPICIOUS_KEYWORDS = [
    "login",
    "signin",
    "sign-in",
    "verify",
    "verification",
    "account",
    "update",
    "banking",
    "secure",
    "security",
    "confirm",
    "wallet",
    "recover",
    "recovery",
    "billing",
    "password",
    "credential",
    "authenticate",
    "support",
    "service",
    "portal",
    "validate",
]

# Targeted high-value brands frequently impersonated in phishing campaigns
TARGET_BRANDS = {
    "paypal": ["paypal.com", "paypal.me"],
    "google": ["google.com", "accounts.google.com"],
    "apple": ["apple.com", "icloud.com"],
    "microsoft": ["microsoft.com", "live.com", "office.com", "outlook.com"],
    "netflix": ["netflix.com"],
    "amazon": ["amazon.com", "amazon.co.uk", "amazon.de"],
    "facebook": ["facebook.com", "fb.com"],
    "instagram": ["instagram.com"],
    "chase": ["chase.com"],
    "wellsfargo": ["wellsfargo.com"],
    "bankofamerica": ["bankofamerica.com"],
    "binance": ["binance.com"],
    "coinbase": ["coinbase.com"],
    "steam": ["steampowered.com", "steamcommunity.com"],
    "adobe": ["adobe.com"],
    "dropbox": ["dropbox.com"],
}

# Known URL shortener services that obscure true destinations
KNOWN_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "rebrand.ly",
    "cutt.ly",
    "goo.gl",
    "bit.do",
    "rotf.lol",
}


def calculate_shannon_entropy(text: str) -> float:
    """Compute the Shannon entropy of a string (in bits per symbol).

    Higher entropy values indicate greater randomness or obfuscation,
    a common indicator of algorithmically generated domains (DGA) or
    encoded payloads.
    """
    if not text:
        return 0.0

    length = len(text)
    counts = Counter(text)
    entropy = 0.0

    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)

    return round(entropy, 4)


def extract_features(parsed: ParsedURL) -> FeatureMetrics:
    """Extract 30 static features from a parsed URL structure."""
    url = parsed.normalized_url
    hostname = parsed.hostname
    path = parsed.path
    query = parsed.query

    # 1. Length & structural metrics
    url_len = len(url)
    host_len = len(hostname)
    path_len = len(path)
    query_len = len(query)

    path_segments = [s for s in path.strip("/").split("/") if s]
    num_path_segments = len(path_segments)

    query_params = [q for q in query.split("&") if q] if query else []
    num_query_params = len(query_params)

    tld_len = len(parsed.suffix)
    subdomain_parts = [p for p in parsed.subdomain.split(".") if p] if parsed.subdomain else []
    subdomain_depth = len(subdomain_parts)

    # 2. Character & symbol counts
    count_dots = url.count(".")
    count_hyphens = url.count("-")
    count_underscores = url.count("_")
    count_slashes = url.count("/")
    count_question = url.count("?")
    count_equals = url.count("=")
    count_at = url.count("@")
    count_percent = url.count("%")
    count_digits = sum(1 for c in url if c.isdigit())
    digit_ratio = round(count_digits / max(1, url_len), 4)

    # 3. Information-theoretic entropy
    entropy_url = calculate_shannon_entropy(url)
    entropy_hostname = calculate_shannon_entropy(hostname)
    entropy_path = calculate_shannon_entropy(path)

    # 4. Keyword & brand impersonation checks
    url_lower = url.lower()
    host_lower = hostname.lower()
    path_query_lower = (path + "?" + query).lower()

    suspicious_keyword_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)

    # Brand checks
    has_brand_subdomain = False
    has_brand_path = False

    for brand, legit_domains in TARGET_BRANDS.items():
        is_official = any(parsed.registered_domain == d.lower() for d in legit_domains)
        if not is_official:
            # If not the official brand domain, inspect if brand is embedded in subdomain
            if brand in parsed.subdomain.lower():
                has_brand_subdomain = True
            # Inspect if brand is embedded in path/query
            if brand in path_query_lower:
                has_brand_path = True

    # 5. Network & protocol properties
    is_shortened = parsed.registered_domain in KNOWN_SHORTENERS
    has_hex = bool(re.search(r"%[0-9a-fA-F]{2}", url))
    is_https = parsed.scheme == "https"
    has_non_standard_port = bool(parsed.port and parsed.port not in (80, 443))

    return FeatureMetrics(
        url_length=url_len,
        hostname_length=host_len,
        path_length=path_len,
        query_length=query_len,
        num_path_segments=num_path_segments,
        num_query_params=num_query_params,
        tld_length=tld_len,
        subdomain_depth=subdomain_depth,
        count_dots=count_dots,
        count_hyphens=count_hyphens,
        count_underscores=count_underscores,
        count_slashes=count_slashes,
        count_question=count_question,
        count_equals=count_equals,
        count_at=count_at,
        count_percent=count_percent,
        count_digits=count_digits,
        digit_ratio=digit_ratio,
        entropy_url=entropy_url,
        entropy_hostname=entropy_hostname,
        entropy_path=entropy_path,
        count_suspicious_keywords=suspicious_keyword_count,
        has_brand_in_subdomain=has_brand_subdomain,
        has_brand_in_path=has_brand_path,
        is_shortened_url=is_shortened,
        has_hex_encoded_char=has_hex,
        is_ip_address=parsed.is_ip_address,
        is_https=is_https,
        has_non_standard_port=has_non_standard_port,
        is_punycode=parsed.is_punycode,
        tld=parsed.suffix,
        domain=parsed.registered_domain,
    )


# Ordered list of numeric feature names used for machine learning models
ML_FEATURE_NAMES: List[str] = [
    "url_length",
    "hostname_length",
    "path_length",
    "query_length",
    "num_path_segments",
    "num_query_params",
    "tld_length",
    "subdomain_depth",
    "count_dots",
    "count_hyphens",
    "count_underscores",
    "count_slashes",
    "count_question",
    "count_equals",
    "count_at",
    "count_percent",
    "count_digits",
    "digit_ratio",
    "entropy_url",
    "entropy_hostname",
    "entropy_path",
    "count_suspicious_keywords",
    "has_brand_in_subdomain",
    "has_brand_in_path",
    "is_shortened_url",
    "has_hex_encoded_char",
    "is_ip_address",
    "is_https",
    "has_non_standard_port",
    "is_punycode",
]


def features_to_vector(features: FeatureMetrics) -> List[float]:
    """Convert FeatureMetrics to an ordered numerical vector for ML inference."""
    vector: List[float] = []
    for feat_name in ML_FEATURE_NAMES:
        val = getattr(features, feat_name)
        if isinstance(val, bool):
            vector.append(1.0 if val else 0.0)
        else:
            vector.append(float(val))
    return vector
