# LINKSHIELD — PROJECT BRAIN (ARCHITECTURAL KNOWLEDGE BASE)

> **Document Status**: Source of Truth  
> **Last Updated**: Phase 0 (Project Foundation)  
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
| **ADR-001** | Backend Framework | **FastAPI (Python 3.14 / 3.11+)** | High performance, native async support, automated OpenAPI documentation, Pydantic type validation. |
| **ADR-002** | Frontend Architecture | **React 18/19 + Vite + TypeScript** | Type safety, rapid HMR development, component reusability, clean API contracts, lightweight production bundle. |
| **ADR-003** | Styling Approach | **Tailored Cyber Vanilla CSS / CSS Modules** | Eliminates Tailwind build configuration bloat while ensuring deep control over cybersecurity design tokens (dark theme, glassmorphism, glowing status badges, high contrast data tables). |
| **ADR-004** | Static vs. Dynamic URL Analysis | **Defensive Static Analysis First** | Visiting malicious domains from the backend introduces SSRF, DNS rebinding, IP banning, and malware exposure. All initial phases evaluate lexical, structural, and cryptographic properties safely. |
| **ADR-005** | ML Algorithm Selection | **Random Forest / Logistic Regression Baseline** | High interpretability, non-linear feature interaction capture, fast inference (<10ms), low memory footprint, resilience to overfitting with proper regularization. |
| **ADR-006** | Risk Scoring Formulation | **Hybrid Weighted Heuristic + ML** | Pure ML models fail on novel zero-day patterns and can output false confidence. Pure heuristics miss complex multi-variable interactions. A hybrid formula provides calibrated 0–100 scores with safety floors. |
| **ADR-007** | Git & Repository Structure | **5-Item Root Invariant** | Keeps root clean, eliminates mixed-package confusion, presents enterprise-level repository discipline for prospective employers. |

---

## 5. Directory Specifications

### 5.1 Backend (`backend/`)
```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── analyze.py
│   │       │   └── health.py
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── engine/
│   │   ├── parser.py          # Safe URL parsing & normalization
│   │   ├── features.py        # 30+ lexical & structural features
│   │   ├── heuristics.py      # Rule-based threat indicators
│   │   ├── risk_scorer.py     # Composite risk formulation
│   │   └── explainer.py       # Human-readable evidence generator
│   ├── ml/
│   │   ├── model_loader.py    # Singleton model inference wrapper
│   │   └── pipeline.py        # Feature transformation pipeline
│   ├── schemas/
│   │   ├── request.py         # URL input validation models
│   │   └── response.py        # AnalysisResult, Indicator, FeatureDetails
│   └── main.py                # FastAPI application entrypoint
├── data/                      # Reference datasets (curated samples / schemas)
├── models/                    # Serialized model weights & scaler artifacts (.joblib)
├── scripts/                   # Training & evaluation scripts (reproducible ML)
├── tests/                     # Pytest suite (unit, integration, edge cases)
├── .env.example               # Environment template
├── .gitignore                 # Backend-specific ignore rules
└── requirements.txt           # Explicit Python dependencies
```

### 5.2 Frontend (`frontend/`)
```text
frontend/
├── public/                    # Static assets, cybersecurity icons, favicon
├── src/
│   ├── assets/                # Visual assets & SVG badges
│   ├── components/            # Reusable UI components
│   │   ├── Header.tsx         # Navigation & system status bar
│   │   ├── UrlInput.tsx       # Interactive URL submission bar with presets
│   │   ├── RiskGauge.tsx      # Radial/circular 0-100 risk score visualizer
│   │   ├── VerdictCard.tsx    # Legitimate/Suspicious/Phishing banner
│   │   ├── FeatureTable.tsx   # Detailed extracted metrics grid
│   │   ├── IndicatorList.tsx  # Red flag & green flag breakdown
│   │   ├── ExplainerBox.tsx   # Actionable defense recommendations
│   │   └── HistoryList.tsx    # Session-based recent scan drawer
│   ├── services/
│   │   └── api.ts             # Axios / Fetch client with error handling
│   ├── types/
│   │   └── index.ts           # TypeScript interfaces matching backend schemas
│   ├── styles/
│   │   ├── variables.css      # Design tokens (cyber dark palette, accents)
│   │   └── index.css          # Global typography and reset styles
│   ├── App.tsx                # Main application orchestrator
│   └── main.tsx               # Entrypoint
├── .env.example               # Frontend environment template (VITE_API_BASE_URL)
├── .gitignore                 # Node/Vite ignore rules
├── index.html                 # HTML shell with proper meta & typography
├── package.json               # Frontend dependencies
├── tsconfig.json              # TypeScript compiler configuration
└── vite.config.ts             # Vite build configuration
```

---

## 6. Risk Scoring & Classification Thresholds

The LinkShield risk engine computes a continuous score in the range `[0, 100]`:

$$\text{Risk Score} = w_{\text{ml}} \times (\text{ML Probability} \times 100) + \sum w_i \times \text{Heuristic Signal}_i$$

The score is clamped between 0 and 100 with fail-safe overrides (e.g., an IP-literal host claiming PayPal automatically triggers a high-severity indicator floor).

| Score Range | Classification | Visual Indicator | Recommended User Action |
|-------------|----------------|-------------------|--------------------------|
| **0 – 25** | `LEGITIMATE` | Neon Cyan / Emerald Green | Safe to proceed; standard security hygiene applies. |
| **26 – 60** | `SUSPICIOUS` | Amber / Warning Orange | Exercise caution; inspect domain identity and avoid entering credentials. |
| **61 – 100** | `PHISHING` | Crimson / Neon Red | **DO NOT VISIT**; deceptive characteristics detected. |

---

## 7. Security Principles for Development

1. **Untrusted Input Guarantee**: Treat all submitted strings as hostile. Strictly limit max length (2048 chars), reject non-HTTP/HTTPS protocols (e.g. `javascript:`, `file:`, `data:`), and sanitize display strings to prevent XSS.
2. **Defensive Isolation**: Never perform automated server-side HTTP `GET`/`POST` requests to arbitrary user-supplied target links.
3. **No Secret Leaks**: Zero hardcoded credentials or API tokens in code. Enforce `.gitignore` vigilance before every commit.
4. **Reliable Degradation**: If the ML model artifact is missing or loading fails, the system must gracefully fall back to heuristic rule scoring rather than crashing the API.

---

## 8. Instructions for Future AI Agents

- **Always verify before altering**: Read `BRAIN.md`, `README.md`, and `ROADMAP.md` at the start of any turn.
- **Never add files to the root**: Place all code, assets, and configs inside `frontend/` or `backend/`.
- **Maintain synchronization**: If backend schemas evolve, immediately update frontend TypeScript types and UI renderers.
- **Test every phase**: Run and verify tests before declaring a milestone complete.
- **Commit with semantic clarity**: Use `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `security:`.
