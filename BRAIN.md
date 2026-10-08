# LINKSHIELD — PROJECT BRAIN (ARCHITECTURAL KNOWLEDGE BASE)

> **Document Status**: Source of Truth  
> **Last Updated**: Production Ready (All 15 Phases Completed)  
> **Repository**: [vyveksharma31/LinkShield](https://github.com/vyveksharma31/LinkShield)  
> **Developer**: Vyvek Sharma (BCA Cybersecurity & Software Development)

---

## 1. Project Purpose & Vision

**LinkShield** is a resume-grade, production-oriented cybersecurity platform designed to detect, analyze, and explain phishing and malicious URLs. 

Unlike basic machine learning demos or simplistic CRUD applications, LinkShield operates as a defense-in-depth security tool. It combines **lexical/structural feature extraction**, **security heuristic indicators**, and **calibrated machine learning models** into a unified **Risk Scoring & Explainability Engine**, delivered via a modern, high-trust cybersecurity operations dashboard.

### Core Objectives
1. **Defensive Static Analysis**: Dissect submitted URLs safely without browsing to malicious web servers (mitigating SSRF, drive-by downloads, and remote execution vulnerabilities).
2. **Multi-Signal Risk Assessment**: Refuse binary black-box labels. Combine ML probabilities, heuristic threat signals, protocol anomalies, and domain structure into a defensible 0–100 risk score.
3. **Transparent Explainability**: Deliver human-understandable and security-actionable reasons behind every classification (flagging specific risk-increasing and risk-reducing factors).
4. **Engineering Rigor**: Maintain clean separation of concerns, high test coverage, robust API contracts, zero-secret repository hygiene, and strict architectural discipline.

---

## 2. Strict Repository Architecture & Root Rule

The repository root **MUST NEVER** contain arbitrary files. It is strictly constrained to exactly five items:

```text
LinkShield/
│
├── frontend/        # React + Vite + TypeScript Cybersecurity Dashboard
├── backend/         # FastAPI, URL Analysis Engine, ML Pipeline & Tests
├── BRAIN.md         # Permanent project memory & architectural specifications
├── README.md        # Comprehensive public documentation & setup guide
└── ROADMAP.md       # Phased project milestones, tasks, and progress tracking
```

### Root Invariant Rules:
- No root `.gitignore`, `.env`, `package.json`, `requirements.txt`, notebooks, or temporary files.
- All dependencies, environment configs, and directory-specific ignore files reside strictly inside `frontend/` or `backend/`.
- Root remains pristine, professional, and compliant with portfolio presentation standards.

---

## 3. System Architecture & Detection Pipeline

```text
                      [ User Input / Client Dashboard ]
                                      │
                                      ▼
                      [ REST API: POST /api/v1/analyze ]
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │      URL Validation & Safety      │
                    │   - Syntactic validation          │
                    │   - Scheme check (http, https)    │
                    │   - Length / character bounds     │
                    │   - Sanitization (anti-SSRF/safe) │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │     URL Normalization & Parsing   │
                    │   - Punycode decoding             │
                    │   - TLD / Domain / Path parsing   │
                    │   - Query parameter dissection    │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │     Feature Extraction Engine     │
                    │   - Lexical & length statistics   │
                    │   - Shannon entropy calculations  │
                    │   - Subdomain & dot count         │
                    │   - Suspicious keyword detection  │
                    │   - IP address host validation    │
                    └─────────┬─────────────────┬───────┘
                              │                 │
              ┌───────────────┘                 └───────────────┐
              ▼                                                 ▼
┌───────────────────────────┐                     ┌───────────────────────────┐
│   Security Heuristics     │                     │     Machine Learning      │
│ - Brand impersonation     │                     │   - Pretrained Classifier │
│ - Obfuscation / encodings │                     │   - Feature scaling/vector│
│ - Free/suspicious TLDs    │                     │   - Probability output    │
│ - Sensitive path keywords │                     │   - Confidence score      │
└─────────────┬─────────────┘                     └─────────────┬─────────────┘
              │                                                 │
              └───────────────┐                 ┌───────────────┘
                              ▼                 ▼
                    ┌───────────────────────────────────┐
                    │       Risk Scoring Engine         │
                    │   Composite 0-100 Risk Score      │
                    │   (ML prob + Heuristic weights)   │
                    │   Classification:                 │
                    │   LEGITIMATE / SUSPICIOUS /       │
                    │   PHISHING                        │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                    ┌───────────────────────────────────┐
                    │       Explainability Engine       │
                    │   - Risk-increasing indicators    │
                    │   - Risk-reducing indicators      │
                    │   - Actionable recommendations    │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                       [ Structured JSON Response ]
                                      │
                                      ▼
                     [ Frontend Cybersecurity UI ]
```

---

## 4. Key Architectural Decisions (ADR Log)

| Decision ID | Topic | Choice | Rationale |
|-------------|-------|--------|-----------|
| **ADR-001** | Backend Framework | **FastAPI (Python 3.11+)** | High performance, native async support, automated OpenAPI documentation, Pydantic type validation. |
| **ADR-002** | Frontend Architecture | **React + Vite + TypeScript** | Type safety, rapid HMR development, component reusability, clean API contracts, lightweight production bundle. |
| **ADR-003** | Styling Approach | **Tailored Cyber Vanilla CSS / CSS Modules** | Eliminates Tailwind build configuration bloat while ensuring deep control over cybersecurity design tokens (dark theme, glassmorphism, glowing status badges, high contrast data tables). |
| **ADR-004** | Static vs. Dynamic URL Analysis | **Defensive Static Analysis First** | Visiting malicious domains from the backend introduces SSRF, DNS rebinding, IP banning, and malware exposure. All initial phases evaluate lexical, structural, and cryptographic properties safely. |
| **ADR-005** | ML Algorithm Selection | **Random Forest / Logistic Regression Baseline** | High interpretability, non-linear feature interaction capture, fast inference (<10ms), low memory footprint, resilience to overfitting with proper regularization. |
| **ADR-006** | Risk Scoring Formulation | **Hybrid Weighted Heuristic + ML** | Pure ML models fail on novel zero-day patterns and can output false confidence. Pure heuristics miss complex multi-variable interactions. A hybrid formula provides calibrated 0–100 scores with safety floors. |
| **ADR-007** | Git & Repository Structure | **5-Item Root Invariant** | Keeps root clean, eliminates mixed-package confusion, presents enterprise-level repository discipline for prospective employers. |

---

## 5. Detailed Specifications & Schemas

### 5.1 REST API Contract (`/api/v1`)

#### 1. Analyze Endpoint: `POST /api/v1/analyze`
**Request Body:**
```json
{
  "url": "https://secure-login.paypal.com.account-update.xyz/verify"
}
```
Validation Constraints:
- Length: Minimum 3 characters, Maximum 2048 characters.
- Must be a valid string conforming to URI syntax. Scheme defaults to `http://` if missing during normalization. Non-HTTP(S) schemes (e.g. `javascript:`, `data:`, `file:`) are rejected with 422 Unprocessable Entity.

**Response Body (`AnalysisResponse`):**
```json
{
  "url": "https://secure-login.paypal.com.account-update.xyz/verify",
  "normalized_url": "https://secure-login.paypal.com.account-update.xyz/verify",
  "verdict": "PHISHING",
  "risk_score": 88,
  "confidence": 0.94,
  "ml_prediction": {
    "phishing_probability": 0.92,
    "raw_label": "phishing",
    "model_version": "rf-v1.0"
  },
  "heuristic_flags": [
    {
      "code": "BRAND_IMPERSONATION",
      "severity": "CRITICAL",
      "category": "Brand Forensics",
      "title": "Brand Impersonation Detected",
      "description": "Targeted brand token 'paypal' was found inside subdomain or path, but registered domain is 'account-update.xyz'",
      "evidence": "paypal in subdomain of account-update.xyz",
      "score_impact": 40
    },
    {
      "code": "SUSPICIOUS_TLD",
      "severity": "HIGH",
      "category": "Domain Forensics",
      "title": "High-Risk Top Level Domain",
      "description": "TLD '.xyz' is frequently associated with disposable malicious infrastructure",
      "evidence": "xyz",
      "score_impact": 20
    }
  ],
  "positive_flags": [
    {
      "category": "Transport Security",
      "title": "Valid HTTPS Scheme",
      "description": "URL specifies HTTPS protocol with standard TLS port."
    }
  ],
  "features": {
    "url_length": 56,
    "hostname_length": 48,
    "path_length": 7,
    "query_length": 0,
    "dot_count": 4,
    "hyphen_count": 2,
    "subdomain_count": 3,
    "is_ip_address": false,
    "entropy_host": 3.42,
    "entropy_path": 2.15,
    "suspicious_keyword_count": 2,
    "tld": "xyz",
    "domain": "account-update.xyz"
  },
  "recommendations": [
    "DO NOT visit or enter credentials on this page.",
    "This URL is impersonating PayPal on an unrelated domain.",
    "Report this domain to the hosting registrar and security vendor."
  ],
  "analyzed_at": "2026-10-06T19:00:00Z",
  "execution_time_ms": 11.2
}
```

#### 2. Health Endpoint: `GET /api/v1/health`
**Response Body:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true,
  "timestamp": "2026-10-06T19:00:00Z"
}
```

---

## 6. Feature Extraction Matrix (30 Features)

Features are extracted statically from the URL string across 5 categories:

1. **Length & Structure Metrics (8)**:
   - `url_length`: Total character count.
   - `hostname_length`: Netloc character count.
   - `path_length`: URL path character count.
   - `query_length`: Query parameters length.
   - `num_path_segments`: Count of `/` delimited path tokens.
   - `num_query_params`: Count of `&` delimited query arguments.
   - `tld_length`: Length of Top-Level Domain string.
   - `subdomain_depth`: Count of subdomains preceding registered domain.

2. **Character & Symbol Frequencies (10)**:
   - `count_dots`: Total occurrences of `.`.
   - `count_hyphens`: Total occurrences of `-`.
   - `count_underscores`: Total occurrences of `_`.
   - `count_slashes`: Total occurrences of `/`.
   - `count_question`: Total occurrences of `?`.
   - `count_equals`: Total occurrences of `=`.
   - `count_at`: Total occurrences of `@` (credential delimiter trick).
   - `count_percent`: Total occurrences of `%` (hex escapes).
   - `count_digits`: Total numeric characters.
   - `digit_ratio`: Ratio of digits to total characters in URL.

3. **Information-Theoretic & Entropy Metrics (3)**:
   - `entropy_url`: Shannon entropy of entire URL string ($H = -\sum p_i \log_2 p_i$).
   - `entropy_hostname`: Shannon entropy of hostname (detects DGA / random generation).
   - `entropy_path`: Shannon entropy of path components.

4. **Threat Keyword & Semantic Indicators (5)**:
   - `count_suspicious_keywords`: Frequency of keywords (`login`, `signin`, `verify`, `account`, `update`, `banking`, `secure`, `confirm`, `wallet`, `recover`, `billing`).
   - `has_brand_in_subdomain`: Target brand found in subdomains.
   - `has_brand_in_path`: Target brand found in path while domain is unrelated.
   - `is_shortened_url`: Matches known URL shortening providers (`bit.ly`, `tinyurl.com`, `t.co`, `ow.ly`, `is.gd`, `buff.ly`).
   - `has_hex_encoded_char`: Presence of hexadecimal encoded patterns.

5. **Network & Protocol Semantics (4)**:
   - `is_ip_address`: Host is an IPv4 or IPv6 address literal.
   - `is_https`: Whether scheme is `https`.
   - `has_non_standard_port`: Authority contains a port other than 80 or 443.
   - `is_punycode`: Host begins with or contains `xn--` (IDN homoglyph indicator).

---

## 7. Security Heuristic Engine Rules

| Code | Severity | Weight | Trigger Condition |
|---|---|---|---|
| `IP_HOST` | **CRITICAL** | +40 | Hostname matches IPv4/IPv6 pattern. Phishers use IP literals to bypass domain registrars. |
| `AT_SYMBOL_OBFUSCATION` | **CRITICAL** | +40 | URL contains `@` before path. RFC 3986 treats prefix as userinfo, masking actual destination. |
| `BRAND_IMPERSONATION` | **CRITICAL** | +45 | High-value brand token in subdomain or path when domain is not the official brand owner. |
| `EXCESSIVE_SUBDOMAINS` | **HIGH** | +25 | Subdomain count $\ge 3$, common in multi-stage phishing redirects. |
| `SUSPICIOUS_TLD` | **HIGH** | +20 | Domain uses known free/high-abuse TLDs (`.tk`, `.ml`, `.ga`, `.cf`, `.gq`, `.top`, `.xyz`, `.work`, `.click`). |
| `HEX_ENCODED_OBFUSCATION` | **MEDIUM** | +15 | URL contains excessive `%` escapes intended to evade signature filters. |
| `AUTH_KEYWORD_PATH` | **MEDIUM** | +15 | Path contains authentication/credential tokens on non-whitelisted domain. |
| `HIGH_HOST_ENTROPY` | **MEDIUM** | +15 | Hostname Shannon entropy exceeds 3.8, indicative of algorithmically generated domain names (DGA). |
| `URL_SHORTENER` | **MEDIUM** | +15 | Known shortening service used to disguise target destination. |
| `NON_STANDARD_PORT` | **LOW** | +10 | Port specified is not standard HTTP(80) or HTTPS(443). |

---

## 8. Hybrid Risk Scoring & Classification Formulation

$$\text{ML Probability} = P(\text{phishing} \mid \vec{x}) \in [0.0, 1.0]$$
$$\text{Heuristic Penalty} = \min\left(50, \sum_{i \in \text{Triggers}} \text{Weight}_i\right)$$
$$\text{Raw Score} = 0.60 \times (\text{ML Probability} \times 100) + 0.40 \times \text{Heuristic Penalty}$$

### Safety Overrides (Failsafes):
1. **Critical Flag Override**: If any `CRITICAL` heuristic is triggered (`IP_HOST`, `AT_SYMBOL_OBFUSCATION`, or `BRAND_IMPERSONATION`), $\text{Score} \leftarrow \max(\text{Raw Score}, 75)$.
2. **Whitelisted Authority Dampener**: If domain is an exact match for a top verified root authority (e.g., `google.com`, `microsoft.com`, `github.com`) and has zero suspicious path keywords, $\text{Score} \leftarrow \min(\text{Raw Score}, 10)$.

### Final Verdict Mapping:
- **0 – 25**: `LEGITIMATE` (Clean indicators, trusted structure)
- **26 – 60**: `SUSPICIOUS` (Anomalous features, caution advised)
- **61 – 100**: `PHISHING` (High malicious probability or critical threat indicators)

---

## 9. Frontend Cyber Design System Specification

### Color Tokens
- `--bg-primary`: `#0a0e17` (Deep Cyber Void)
- `--bg-secondary`: `#111827` (Tactical Panel Grey)
- `--bg-tertiary`: `#1e293b` (Elevated Card Background)
- `--border-subtle`: `#334155` (Panel Borders)
- `--border-glow`: `rgba(6, 182, 212, 0.3)` (Electric Accent Glow)
- `--accent-cyan`: `#06b6d4` (Terminal Cyan)
- `--accent-emerald`: `#10b981` (Legitimate / Safe)
- `--accent-amber`: `#f59e0b` (Suspicious / Warning)
- `--accent-crimson`: `#ef4444` (Phishing / Critical Threat)
- `--text-primary`: `#f8fafc` (Bright Tactical White)
- `--text-secondary`: `#94a3b8` (Muted Technical Grey)
- `--font-mono`: `'JetBrains Mono', 'Fira Code', 'Courier New', monospace`
- `--font-sans`: `'Inter', system-ui, -apple-system, sans-serif`

---

## 10. Security Hardening Principles

1. **Static Analysis Only**: No outbound network requests are made to analyze target websites. Zero chance of server compromise via SSRF.
2. **Untrusted Input Sanitation**: Length limits (max 2048), scheme restrictions, and HTML escaping prevent payload injection.
3. **Graceful Fail-Soft**: If model weights are missing, the heuristic engine continues to provide accurate risk assessments without crashing.

---

## 11. Final Verification & Quality Assurance Benchmarks

- **Automated Test Suite**: 147 test cases total (141 backend Pytest + 6 frontend Vitest), 100% passing rate with 0 warnings.
- **Latency Benchmarks**: 13.13 ms average response time across 100 diverse real-world URL requests (exceeding the <30ms performance target).
- **Anti-SSRF Assurance**: Socket interception tests verify zero network connection attempts during analysis.
- **Production Bundle**: Optimized code splitting with lightweight initial JavaScript bundle (~151 kB / 48 kB gzip).
- **Clean Root Invariant**: Strictly enforced 5 items in repository root (`frontend/`, `backend/`, `BRAIN.md`, `README.md`, `ROADMAP.md`).
