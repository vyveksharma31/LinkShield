"""Unit tests for the rule-based security threat heuristics engine."""
import pytest
from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features
from backend.app.engine.heuristics import evaluate_heuristics, SUSPICIOUS_TLDS, TRUSTED_AUTHORITIES
from backend.app.schemas.response import SeverityEnum


def test_ip_host_heuristic():
    """Verify IP_HOST triggers CRITICAL severity and +40 impact."""
    parsed = normalize_and_parse_url("http://192.168.1.100/admin")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert result.has_critical_flag is True
    assert any(f.code == "IP_HOST" and f.severity == SeverityEnum.CRITICAL for f in result.heuristic_flags)


def test_at_symbol_obfuscation_heuristic():
    """Verify AT_SYMBOL_OBFUSCATION triggers CRITICAL severity on credential delimiter."""
    parsed = normalize_and_parse_url("http://bank.com@evil-site.com/auth")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert result.has_critical_flag is True
    assert any(f.code == "AT_SYMBOL_OBFUSCATION" and f.severity == SeverityEnum.CRITICAL for f in result.heuristic_flags)


def test_homoglyph_spoofing_heuristic():
    """Verify HOMOGLYPH_SPOOFING triggers CRITICAL severity on IDN confusable."""
    parsed = normalize_and_parse_url("https://xn--pypal-4ve.com/signin")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert result.has_critical_flag is True
    assert any(f.code == "HOMOGLYPH_SPOOFING" and f.severity == SeverityEnum.CRITICAL for f in result.heuristic_flags)


def test_brand_impersonation_subdomain():
    """Verify BRAND_IMPERSONATION triggers when high-value brand is in subdomain."""
    parsed = normalize_and_parse_url("https://paypal.secure-login-account.com/verify")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert result.has_critical_flag is True
    assert any(f.code == "BRAND_IMPERSONATION" and f.score_impact == 45 for f in result.heuristic_flags)


def test_brand_impersonation_path():
    """Verify BRAND_IMPERSONATION triggers when brand token is embedded in untrusted path."""
    parsed = normalize_and_parse_url("http://untrusted-portal.com/apple/icloud-restore")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert result.has_critical_flag is True
    assert any(f.code == "BRAND_IMPERSONATION" for f in result.heuristic_flags)


def test_excessive_subdomains_heuristic():
    """Verify EXCESSIVE_SUBDOMAINS triggers on 3 or more subdomain levels."""
    parsed = normalize_and_parse_url("https://a.b.c.target-bank.example.com/")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert any(f.code == "EXCESSIVE_SUBDOMAINS" and f.severity == SeverityEnum.HIGH for f in result.heuristic_flags)


def test_suspicious_tld_heuristic():
    """Verify SUSPICIOUS_TLD triggers on high-abuse top-level domains."""
    for tld in ["xyz", "top", "tk", "work", "click"]:
        parsed = normalize_and_parse_url(f"http://account-update-notice.{tld}/login")
        features = extract_features(parsed)
        result = evaluate_heuristics(parsed, features)
        assert any(f.code == "SUSPICIOUS_TLD" and f.severity == SeverityEnum.HIGH for f in result.heuristic_flags)


def test_hex_encoded_obfuscation_heuristic():
    """Verify HEX_ENCODED_OBFUSCATION triggers on multiple or evasive percent encodings."""
    parsed = normalize_and_parse_url("http://example.com/%70%61%79%70%61%6c/path")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert any(f.code == "HEX_ENCODED_OBFUSCATION" and f.severity == SeverityEnum.MEDIUM for f in result.heuristic_flags)


def test_auth_keyword_path_heuristic():
    """Verify AUTH_KEYWORD_PATH triggers when 2 or more sensitive lure keywords appear."""
    parsed = normalize_and_parse_url("http://sample-site.net/login/verify/account")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert any(f.code == "AUTH_KEYWORD_PATH" and f.severity == SeverityEnum.MEDIUM for f in result.heuristic_flags)


def test_url_shortener_heuristic():
    """Verify URL_SHORTENER triggers on recognized shortener domains."""
    parsed = normalize_and_parse_url("https://bit.ly/secure-redirect")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert any(f.code == "URL_SHORTENER" and f.severity == SeverityEnum.MEDIUM for f in result.heuristic_flags)


def test_non_standard_port_heuristic():
    """Verify NON_STANDARD_PORT triggers when port is not 80 or 443."""
    parsed = normalize_and_parse_url("http://example.com:8080/app")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert any(f.code == "NON_STANDARD_PORT" and f.severity == SeverityEnum.LOW for f in result.heuristic_flags)


def test_legitimate_authority_positive_flags():
    """Verify legitimate trusted authority receives positive flags and zero critical heuristics."""
    parsed = normalize_and_parse_url("https://github.com/vyveksharma31/LinkShield")
    features = extract_features(parsed)
    result = evaluate_heuristics(parsed, features)

    assert result.has_critical_flag is False
    assert result.is_whitelisted_authority is True
    assert len(result.heuristic_flags) == 0
    assert any(p.title == "Verified Global Authority" for p in result.positive_flags)
    assert any(p.title == "Valid HTTPS Transport" for p in result.positive_flags)
