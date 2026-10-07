"""Safe static URL parser and normalizer.

This module performs purely static parsing, normalization, and structural decomposition
without executing network calls, preventing SSRF and external execution hazards.
"""
import ipaddress
import re
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from urllib.parse import urlparse, unquote
import tldextract


# Common Cyrillic and Greek homoglyphs used in IDN spoofing attacks
HOMOGLYPH_MAP: dict[str, str] = {
    # Cyrillic lowercase
    "\u0430": "a", "\u0441": "c", "\u0435": "e", "\u043e": "o", "\u0440": "p",
    "\u0455": "s", "\u0445": "x", "\u0443": "y", "\u0456": "i", "\u0458": "j",
    "\u0501": "d", "\u051b": "q", "\u051d": "w",
    # Cyrillic uppercase
    "\u0410": "A", "\u0412": "B", "\u0421": "C", "\u0415": "E", "\u041d": "H",
    "\u0406": "I", "\u0408": "J", "\u041a": "K", "\u041c": "M", "\u041e": "O",
    "\u0420": "P", "\u0422": "T", "\u0425": "X",
    # Greek lowercase
    "\u03b1": "a", "\u03b2": "b", "\u03b5": "e", "\u03b9": "i", "\u03ba": "k",
    "\u03bd": "v", "\u03bf": "o", "\u03c1": "p", "\u03c4": "t", "\u03c5": "u",
    "\u03c7": "x",
}


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
    has_homoglyphs: bool = False
    homoglyphs_detected: List[str] = field(default_factory=list)
    has_userinfo: bool = False


# Offline tldextract instance that avoids runtime network downloads
_extractor = tldextract.TLDExtract(cache_dir=None, suffix_list_urls=None)


def detect_homoglyphs(text: str) -> Tuple[bool, List[str]]:
    """Detect presence of Unicode homoglyphs commonly used in IDN spoofing."""
    found: List[str] = []
    for char in text:
        if char in HOMOGLYPH_MAP:
            found.append(char)
    return len(found) > 0, found


def is_ip_host(host: str) -> Tuple[bool, Optional[int]]:
    """Determine if a hostname is an IPv4 or IPv6 address literal across formats."""
    clean_host = host.strip("[]")
    if not clean_host:
        return False, None

    # 1. Standard decimal IPv4 or IPv6 literal
    try:
        ip = ipaddress.ip_address(clean_host)
        return True, ip.version
    except ValueError:
        pass

    # 2. Hex dotted IPv4 representation (e.g. 0x7f.0x00.0x00.0x01)
    if re.fullmatch(r"(?:0x[0-9a-fA-F]+\.){3}0x[0-9a-fA-F]+", clean_host):
        try:
            parts = [int(p, 16) for p in clean_host.split(".")]
            if all(0 <= p <= 255 for p in parts):
                return True, 4
        except ValueError:
            pass

    # 3. Dotted notation with octal or mixed bases (e.g. 0177.0.0.1 or 0177.0.0.01)
    dotted_parts = clean_host.split(".")
    if len(dotted_parts) == 4:
        try:
            parsed_octets = []
            has_alternative_format = False
            for p in dotted_parts:
                if not p:
                    break
                if p.startswith(("0x", "0X")):
                    parsed_octets.append(int(p, 16))
                    has_alternative_format = True
                elif p.startswith("0") and len(p) > 1 and all(c in "01234567" for c in p):
                    parsed_octets.append(int(p, 8))
                    has_alternative_format = True
                elif p.isdigit():
                    parsed_octets.append(int(p, 10))
                else:
                    break
            if len(parsed_octets) == 4 and all(0 <= o <= 255 for o in parsed_octets):
                return True, 4
        except (ValueError, OverflowError):
            pass

    # 4. Hex integer representation (e.g. 0x7f000001)
    if re.fullmatch(r"0x[0-9a-fA-F]{1,8}", clean_host):
        try:
            val = int(clean_host, 16)
            if 0 <= val <= 0xFFFFFFFF:
                ip = ipaddress.ip_address(val)
                return True, ip.version
        except (ValueError, OverflowError):
            pass

    # 5. Decimal dword integer representation (e.g. 2130706433)
    if re.fullmatch(r"\d{8,10}", clean_host):
        try:
            val = int(clean_host, 10)
            if 0 <= val <= 0xFFFFFFFF:
                ip = ipaddress.ip_address(val)
                return True, ip.version
        except (ValueError, OverflowError):
            pass

    return False, None


def normalize_and_parse_url(raw_url: str) -> ParsedURL:
    """Safely sanitize, normalize, and parse a raw URL string."""
    cleaned = raw_url.strip()
    if not cleaned:
        raise ValueError("URL cannot be empty.")

    # Guard against oversized URLs (DoS prevention)
    if len(cleaned) > 2048:
        raise ValueError("URL exceeds maximum allowed length of 2048 characters.")

    # Guard against null bytes and illegal control characters
    if any(ord(c) < 32 or ord(c) == 127 for c in cleaned):
        raise ValueError("URL contains invalid control characters or null bytes.")

    # Reject dangerous pseudo-schemes
    lower_raw = cleaned.lower()
    for forbidden in (
        "javascript:", "data:", "file:", "vbscript:", "blob:",
        "about:", "chrome:", "view-source:", "ws:", "wss:", "ftp:",
    ):
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
    has_userinfo = "@" in netloc

    hostname = parsed.hostname or ""
    if not hostname:
        raise ValueError("URL must contain a valid hostname.")

    port = parsed.port
    path = parsed.path or "/"
    query = parsed.query or ""
    fragment = parsed.fragment or ""

    # Punycode check & decoding / IDN resolution
    is_punycode = "xn--" in hostname.lower()
    decoded_hostname = hostname

    # Handle internationalized domain names (IDN)
    if not is_punycode:
        try:
            encoded_idna = hostname.encode("idna").decode("ascii")
            if "xn--" in encoded_idna:
                is_punycode = True
        except Exception:
            pass

    if is_punycode:
        try:
            decoded_hostname = hostname.encode("ascii").decode("idna")
        except Exception:
            decoded_hostname = hostname

    has_homoglyphs, homoglyphs_found = detect_homoglyphs(decoded_hostname)

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
        reg_domain = getattr(ext, "top_domain_under_public_suffix", "")
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
        has_homoglyphs=has_homoglyphs,
        homoglyphs_detected=homoglyphs_found,
        has_userinfo=has_userinfo,
    )

