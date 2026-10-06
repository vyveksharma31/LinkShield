"""Safe static URL parser and normalizer.

This module performs purely static parsing, normalization, and structural decomposition
without executing network calls, preventing SSRF and external execution hazards.
"""
import ipaddress
import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse
import tldextract


@dataclass
class ParsedURL:
    """Decomposed structural representation of a normalized URL."""

    original_url: str
    normalized_url: str
    scheme: str
    netloc: str
    hostname: str
    port: Optional[int]
    path: str
    query: str
    fragment: str
    subdomain: str
    domain: str
    suffix: str
    registered_domain: str
    is_ip_address: bool
    ip_version: Optional[int]
    is_punycode: bool
    decoded_hostname: str


# Offline tldextract instance that avoids runtime network downloads
_extractor = tldextract.TLDExtract(cache_dir=None, suffix_list_urls=None)


def is_ip_host(host: str) -> tuple[bool, Optional[int]]:
    """Determine if a hostname is an IPv4 or IPv6 address literal."""
    clean_host = host.strip("[]")
    try:
        ip = ipaddress.ip_address(clean_host)
        return True, ip.version
    except ValueError:
        pass

    # Check for integer or hex representation of IP addresses (e.g. 0x7f.0x00.0x00.0x01 or dword IP)
    if re.fullmatch(r"(?:0x[0-9a-fA-F]+\.){3}0x[0-9a-fA-F]+", clean_host):
        return True, 4
    if re.fullmatch(r"\d{8,10}", clean_host):
        # 32-bit integer IP representation
        try:
            ip = ipaddress.ip_address(int(clean_host))
            return True, ip.version
        except (ValueError, OverflowError):
            pass

    return False, None


def normalize_and_parse_url(raw_url: str) -> ParsedURL:
    """Safely sanitize, normalize, and parse a raw URL string."""
    cleaned = raw_url.strip()
    if not cleaned:
        raise ValueError("URL cannot be empty.")

    # Reject dangerous pseudo-schemes
    lower_raw = cleaned.lower()
    for forbidden in ("javascript:", "data:", "file:", "vbscript:", "blob:"):
        if lower_raw.startswith(forbidden):
            raise ValueError(f"Forbidden URL scheme '{forbidden}' cannot be analyzed.")

    # Supply default scheme if absent for parsing
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+\-.]*://", cleaned):
        normalized = "http://" + cleaned
    else:
        normalized = cleaned

    parsed = urlparse(normalized)
    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"Unsupported protocol scheme '{scheme}'. Only HTTP and HTTPS are permitted.")

    netloc = parsed.netloc or ""
    hostname = parsed.hostname or ""
    port = parsed.port

    path = parsed.path or "/"
    query = parsed.query or ""
    fragment = parsed.fragment or ""

    # Punycode check & decoding
    is_punycode = "xn--" in hostname.lower()
    decoded_hostname = hostname
    if is_punycode:
        try:
            decoded_hostname = hostname.encode("ascii").decode("idna")
        except Exception:
            decoded_hostname = hostname

    # IP address check
    is_ip, ip_ver = is_ip_host(hostname)

    # Extract domain and subdomain components
    if is_ip:
        subdomain = ""
        domain = hostname
        suffix = ""
        registered_domain = hostname
    else:
        ext = _extractor(hostname)
        subdomain = ext.subdomain or ""
        domain = ext.domain or ""
        suffix = ext.suffix or ""
        # Prefer new tldextract property to avoid deprecation warning
        reg_domain = getattr(ext, "top_domain_under_public_suffix", None)
        if not reg_domain:
            reg_domain = getattr(ext, "registered_domain", None)
        registered_domain = reg_domain or hostname

    return ParsedURL(
        original_url=raw_url,
        normalized_url=normalized,
        scheme=scheme,
        netloc=netloc,
        hostname=hostname.lower(),
        port=port,
        path=path,
        query=query,
        fragment=fragment,
        subdomain=subdomain.lower(),
        domain=domain.lower(),
        suffix=suffix.lower(),
        registered_domain=registered_domain.lower(),
        is_ip_address=is_ip,
        ip_version=ip_ver,
        is_punycode=is_punycode,
        decoded_hostname=decoded_hostname.lower(),
    )
