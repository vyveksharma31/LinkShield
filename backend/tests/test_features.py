"""Comprehensive feature extraction tests across 50+ diverse and edge-case URLs."""
import math
import pytest
from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features, features_to_vector, ML_FEATURE_NAMES
from backend.app.schemas.response import FeatureMetrics


# 50+ diverse URLs across legitimate, deceptive, malicious, and structural extremes
TEST_URL_CORPUS = [
    # Top Legitimate Domains
    "https://www.google.com/search?q=cybersecurity",
    "https://github.com/vyveksharma31/LinkShield",
    "https://en.wikipedia.org/wiki/Phishing",
    "https://apple.com/iphone-16",
    "https://microsoft.com/en-us/security",
    "https://aws.amazon.com/console/",
    "https://www.cloudflare.com/products/zero-trust/",
    "https://stackoverflow.com/questions/tagged/python",
    "https://developer.mozilla.org/en-US/docs/Web/HTTP",
    "https://fastapi.tiangolo.com/tutorial/first-steps/",

    # Brand Impersonation in Subdomains
    "https://paypal.secure-verification-portal.com/login",
    "https://apple.id-support-recover-account.net/verify",
    "https://chase.online-banking-access.org/auth",
    "https://microsoft.account-reset-pass.xyz/signin",
    "https://netflix.billing-update-center.click/account",
    "https://binance.wallet-validation-portal.com/security",
    "https://coinbase.pro-recovery-service.top/confirm",
    "https://amazon.order-cancellation-notice.work/review",

    # Brand Impersonation in Path / Query
    "http://evil-tracker.com/paypal/signin/verify.php",
    "http://untrusted-host.net/service/apple/icloud-login",
    "http://phish-lab.xyz/auth?target=chase&action=login",
    "http://cdn-proxy.online/microsoft/office365/portal",

    # IP Address Literal Hosts (IPv4, Hex, Octal, Dword, Non-standard Ports)
    "http://192.168.1.1/admin/login",
    "http://10.0.0.1:8080/portal/auth",
    "http://172.16.254.1:8443/secure",
    "http://0x7f.0x00.0x00.0x01/login",
    "http://0177.0.0.1/verify",
    "http://2130706433/account",
    "http://192.168.10.50:9090/service?token=12345",

    # Credential Delimiter Trick (@ symbol in authority)
    "http://paypal.com@evil-attacker-site.com/login",
    "http://google.com@192.168.1.100/verify",
    "https://chase.com:welcome@banking-portal-fake.xyz/",
    "http://user:password@legit-looking.com.phish.org/auth",

    # URL Shorteners
    "https://bit.ly/3xCyberReport",
    "https://tinyurl.com/secure-login-doc",
    "https://t.co/X89jKwQ0",
    "https://cutt.ly/phishLure",
    "https://is.gd/walletRestore",
    "https://buff.ly/updateNotice",

    # High-Risk / Suspicious TLDs
    "http://account-alert.xyz/verify",
    "http://urgent-notice.top/banking",
    "http://free-gift-crypto.tk/claim",
    "http://system-validator.work/auth",
    "http://cloud-storage-file.click/download",

    # Excessive Subdomain Depth
    "http://a.b.c.d.e.f.secure-bank.example.com/login",
    "https://portal.stage.dev.test.auth.internal-spoof.net/",
    "http://1.2.3.4.5.sub.evil.org/phish",

    # Encoded Patterns & Obfuscation
    "http://phish.net/page%20with%20spaces/index.html",
    "http://target.com/path%2e%2e%2fadmin%2fcredentials",
    "http://example.com/query?param=%3Cscript%3Ealert%281%29%3C%2Fscript%3E",
    "http://host.xyz/%70%61%79%70%61%6c/login",

    # IDN Homoglyphs and Punycode
    "https://xn--pypal-4ve.com/signin",
    "https://xn--appl-43a.com/id",
    "https://xn--googl-r0a.com/search",

    # DGA and High Entropy Hostnames
    "http://xkq9m2w8znv7b4p1.com/beacon",
    "http://7b9f3a2c8e1d5046.biz/gate.php",
    "http://zxcasdqwe123987456.cc/payload",

    # Minimal and Edge Path Structures
    "http://a.co",
    "https://t.me/channel",
    "http://localhost:3000/api",
    "https://example.org/",
    "https://example.org/path/subpath/subpath2/deep/deeper/resource.html?a=1&b=2&c=3&d=4",
]


def test_corpus_size_exceeds_fifty():
    """Verify test corpus contains at least 50 URLs."""
    assert len(TEST_URL_CORPUS) >= 50


@pytest.mark.parametrize("url", TEST_URL_CORPUS)
def test_feature_extraction_pipeline_succeeds(url: str):
    """Verify that feature extraction completes cleanly without errors on all 50+ URLs."""
    parsed = normalize_and_parse_url(url)
    features = extract_features(parsed)

    # Validate output type
    assert isinstance(features, FeatureMetrics)

    # Validate length invariants
    assert features.url_length > 0
    assert features.hostname_length > 0
    assert features.path_length >= 1
    assert features.query_length >= 0

    # Validate symbol count invariants
    assert features.count_dots >= 0
    assert features.count_hyphens >= 0
    assert features.count_underscores >= 0
    assert features.count_slashes >= 0
    assert features.count_digits >= 0
    assert 0.0 <= features.digit_ratio <= 1.0

    # Validate entropy metrics
    assert features.entropy_url >= 0.0
    assert features.entropy_hostname >= 0.0
    assert features.entropy_path >= 0.0

    # Validate ML vector serialization
    vector = features_to_vector(features)
    assert len(vector) == len(ML_FEATURE_NAMES)
    assert len(vector) == 30
    for v in vector:
        assert isinstance(v, (int, float))
        assert not math.isnan(v)
        assert not math.isinf(v)


def test_specific_brand_in_subdomain_feature():
    """Verify has_brand_in_subdomain activates on spoofed subdomain."""
    parsed = normalize_and_parse_url("https://paypal.verification-center.com/login")
    features = extract_features(parsed)
    assert features.has_brand_in_subdomain is True
    assert features.has_brand_in_path is False


def test_official_brand_not_flagged_as_brand_subdomain():
    """Verify official brand domain does NOT trigger impersonation feature."""
    parsed = normalize_and_parse_url("https://paypal.com/signin")
    features = extract_features(parsed)
    assert features.has_brand_in_subdomain is False
    assert features.has_brand_in_path is False


def test_shortener_feature():
    """Verify is_shortened_url activates for recognized shorteners."""
    parsed = normalize_and_parse_url("https://bit.ly/fakeLure")
    features = extract_features(parsed)
    assert features.is_shortened_url is True

    parsed_legit = normalize_and_parse_url("https://wikipedia.org/wiki/Cyber")
    features_legit = extract_features(parsed_legit)
    assert features_legit.is_shortened_url is False


def test_hex_encoded_feature():
    """Verify has_hex_encoded_char triggers on % hex sequences."""
    parsed = normalize_and_parse_url("http://example.com/user%20login")
    features = extract_features(parsed)
    assert features.has_hex_encoded_char is True
    assert features.count_percent == 1


def test_non_standard_port_feature():
    """Verify has_non_standard_port identifies custom ports."""
    parsed_std = normalize_and_parse_url("http://example.com:80/home")
    features_std = extract_features(parsed_std)
    assert features_std.has_non_standard_port is False

    parsed_custom = normalize_and_parse_url("http://example.com:8888/home")
    features_custom = extract_features(parsed_custom)
    assert features_custom.has_non_standard_port is True
