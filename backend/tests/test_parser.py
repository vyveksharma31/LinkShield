"""Unit tests for safe URL parsing, normalization, and IDN/homoglyph resolution."""
import pytest
from backend.app.engine.parser import (
    normalize_and_parse_url,
    is_ip_host,
    detect_homoglyphs,
    ParsedURL,
)


def test_standard_https_url():
    """Verify parsing of standard legitimate HTTPS URL."""
    parsed = normalize_and_parse_url("https://www.github.com/vyveksharma31/LinkShield")
    assert parsed.scheme == "https"
    assert parsed.hostname == "www.github.com"
    assert parsed.subdomain == "www"
    assert parsed.domain == "github"
    assert parsed.suffix == "com"
    assert parsed.registered_domain == "github.com"
    assert parsed.path == "/vyveksharma31/LinkShield"
    assert parsed.is_ip_address is False
    assert parsed.port is None
    assert parsed.has_userinfo is False


def test_missing_scheme_defaults_to_http():
    """Verify that a URL missing a protocol scheme defaults to http."""
    parsed = normalize_and_parse_url("example.com/test?query=1")
    assert parsed.scheme == "http"
    assert parsed.hostname == "example.com"
    assert parsed.domain == "example"
    assert parsed.query == "query=1"


def test_uppercase_normalization():
    """Verify that scheme and hostname are normalized to lowercase."""
    parsed = normalize_and_parse_url("HTTPS://SECURE.BANKING.EXAMPLE.ORG/LOGIN")
    assert parsed.scheme == "https"
    assert parsed.hostname == "secure.banking.example.org"
    assert parsed.subdomain == "secure.banking"
    assert parsed.registered_domain == "example.org"
    assert parsed.path == "/LOGIN"


def test_multi_part_tld_extraction():
    """Verify correct handling of multi-part country code TLDs like co.uk."""
    parsed = normalize_and_parse_url("https://portal.service.amazon.co.uk/orders")
    assert parsed.registered_domain == "amazon.co.uk"
    assert parsed.domain == "amazon"
    assert parsed.suffix == "co.uk"
    assert parsed.subdomain == "portal.service"


def test_non_standard_port():
    """Verify detection and extraction of non-standard port."""
    parsed = normalize_and_parse_url("http://192.168.1.50:8080/admin")
    assert parsed.port == 8080
    assert parsed.is_ip_address is True
    assert parsed.ip_version == 4


def test_ipv4_host_detection():
    """Verify standard IPv4 host identification."""
    is_ip, ver = is_ip_host("192.168.1.1")
    assert is_ip is True
    assert ver == 4

    parsed = normalize_and_parse_url("http://10.0.0.1/dashboard")
    assert parsed.is_ip_address is True
    assert parsed.ip_version == 4
    assert parsed.registered_domain == "10.0.0.1"


def test_ipv6_host_detection():
    """Verify standard IPv6 host identification."""
    is_ip, ver = is_ip_host("[::1]")
    assert is_ip is True
    assert ver == 6

    is_ip_raw, ver_raw = is_ip_host("2001:db8::1")
    assert is_ip_raw is True
    assert ver_raw == 6


def test_hex_dotted_ip_detection():
    """Verify hex-dotted IPv4 representation (e.g. 0x7f.0x00.0x00.0x01)."""
    is_ip, ver = is_ip_host("0x7f.0x00.0x00.0x01")
    assert is_ip is True
    assert ver == 4

    parsed = normalize_and_parse_url("http://0x7f.0x00.0x00.0x01/login")
    assert parsed.is_ip_address is True


def test_octal_dotted_ip_detection():
    """Verify octal-dotted IPv4 representation (e.g. 0177.0.0.1)."""
    is_ip, ver = is_ip_host("0177.0.0.1")
    assert is_ip is True
    assert ver == 4

    parsed = normalize_and_parse_url("http://0177.0.0.1/verify")
    assert parsed.is_ip_address is True


def test_dword_integer_ip_detection():
    """Verify 32-bit dword decimal representation of IPv4."""
    # 2130706433 = 127.0.0.1
    is_ip, ver = is_ip_host("2130706433")
    assert is_ip is True
    assert ver == 4

    parsed = normalize_and_parse_url("http://2130706433/path")
    assert parsed.is_ip_address is True


def test_hex_integer_ip_detection():
    """Verify hex 32-bit integer representation of IPv4."""
    # 0x7f000001 = 127.0.0.1
    is_ip, ver = is_ip_host("0x7f000001")
    assert is_ip is True
    assert ver == 4


def test_non_ip_hostnames():
    """Verify standard alphabetic hostnames are never misclassified as IP addresses."""
    assert is_ip_host("google.com")[0] is False
    assert is_ip_host("sub.domain.co.uk")[0] is False
    assert is_ip_host("123fakestreet.com")[0] is False


def test_punycode_and_homoglyph_detection():
    """Verify decoding and homoglyph flag on punycode domain spoofing paypal."""
    # xn--pypal-4ve.com decodes to pаypal.com with Cyrillic 'а' (U+0430)
    parsed = normalize_and_parse_url("https://xn--pypal-4ve.com/signin")
    assert parsed.is_punycode is True
    assert "xn--" in parsed.hostname
    assert parsed.decoded_hostname == "pаypal.com"
    assert parsed.has_homoglyphs is True
    assert "\u0430" in parsed.homoglyphs_detected


def test_unicode_idn_homoglyph_input():
    """Verify that direct Unicode IDN with homoglyphs is detected."""
    # Cyrillic 'а' in paypal
    unicode_url = "https://pаypal.com/security"
    parsed = normalize_and_parse_url(unicode_url)
    assert parsed.has_homoglyphs is True
    assert parsed.is_punycode is True


def test_homoglyph_detector_clean_text():
    """Verify that pure ASCII strings have zero homoglyphs."""
    has_hg, chars = detect_homoglyphs("paypal.com")
    assert has_hg is False
    assert len(chars) == 0


def test_userinfo_credentials_in_authority():
    """Verify detection of @ credential delimiter evasion trick."""
    parsed = normalize_and_parse_url("http://legitimate-bank.com@evil-attacker.com/login")
    assert parsed.has_userinfo is True
    assert parsed.hostname == "evil-attacker.com"
    assert "legitimate-bank.com@" in parsed.netloc


def test_reject_dangerous_schemes():
    """Verify rejection of non-web schemes and dangerous pseudo-schemes."""
    dangerous = [
        "javascript:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "file:///etc/passwd",
        "vbscript:msgbox(1)",
        "blob:http://example.com/uuid",
        "about:blank",
        "chrome://settings",
        "view-source:https://google.com",
        "ftp://ftp.is.co.za",
        "ws://echo.websocket.org",
        "wss://secure.websocket.org",
    ]
    for url in dangerous:
        with pytest.raises(ValueError, match="Forbidden URL scheme"):
            normalize_and_parse_url(url)


def test_reject_empty_or_whitespace():
    """Verify rejection of empty or blank strings."""
    with pytest.raises(ValueError, match="URL cannot be empty"):
        normalize_and_parse_url("")
    with pytest.raises(ValueError, match="URL cannot be empty"):
        normalize_and_parse_url("   \t  ")


def test_reject_oversized_url():
    """Verify rejection of URLs exceeding 2048 characters."""
    oversized = "https://example.com/" + "a" * 2050
    with pytest.raises(ValueError, match="exceeds maximum allowed length"):
        normalize_and_parse_url(oversized)


def test_reject_control_characters_and_null_bytes():
    """Verify rejection of null bytes and ASCII control characters."""
    with pytest.raises(ValueError, match="invalid control characters or null bytes"):
        normalize_and_parse_url("https://example.com/path\x00evil")
    with pytest.raises(ValueError, match="invalid control characters or null bytes"):
        normalize_and_parse_url("https://example.com/\r\nevil")


def test_reject_missing_hostname():
    """Verify rejection when no valid hostname exists."""
    with pytest.raises(ValueError, match="valid hostname"):
        normalize_and_parse_url("http://")
    with pytest.raises(ValueError, match="valid hostname"):
        normalize_and_parse_url("http:///only/path")
