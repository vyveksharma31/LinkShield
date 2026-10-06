# 🗺️ LINKSHIELD — MASTER DEVELOPMENT ROADMAP

> **Tracking Document**: Project Progression & Milestone Completion  
> **Source of Truth**: Aligned with `BRAIN.md` and `README.md`  
> **Repository**: [vyveksharma31/LinkShield](https://github.com/vyveksharma31/LinkShield)

---

## Overview of Development Phases

| Phase | Title | Status | Description |
|---|---|---|---|
| **Phase 0** | Project Foundation & Hygiene | 🟢 Completed | Environment audit, Git remote verification, core docs, 5-item root enforcement. |
| **Phase 1** | Architecture & Specifications | 🟡 In Progress | Modular subsystem contracts, data schemas, ML pipeline design, security perimeter. |
| **Phase 2** | Backend Foundation | ⚪ Pending | FastAPI setup, API versioning, health endpoints, logging, error handling. |
| **Phase 3** | URL Analysis & Normalization Engine | ⚪ Pending | Safe parsing, punycode decoding, lexical feature extraction (30+ metrics). |
| **Phase 4** | Security Threat Heuristics | ⚪ Pending | Brand impersonation, IP host detection, entropy, suspicious TLD rules. |
| **Phase 5** | Dataset & ML Pipeline | ⚪ Pending | Curated dataset, reproducible train/eval script, model serialization. |
| **Phase 6** | Composite Risk Scoring Engine | ⚪ Pending | Multi-signal weighted risk formula (0–100 scale), confidence calibration. |
| **Phase 7** | Explainability & Recommendation Engine | ⚪ Pending | Structured evidence generation, positive/negative indicators, defense guidance. |
| **Phase 8** | Frontend Cyber Dashboard | ⚪ Pending | React + Vite + TypeScript, cyber design tokens, risk gauge, analysis UI. |
| **Phase 9** | Frontend & Backend Integration | ⚪ Pending | Live API client integration, state management, end-to-end verification. |
| **Phase 10** | Security Hardening & Edge Cases | ⚪ Pending | Input validation, anti-SSRF static checks, CORS, oversized request protection. |
| **Phase 11** | Comprehensive Automated Testing | ⚪ Pending | Pytest unit/integration tests, edge cases (IDN homoglyphs, malformed input). |
| **Phase 12** | Performance & Latency Optimization | ⚪ Pending | Sub-15ms feature extraction, efficient ML loading, asset compression. |
| **Phase 13** | Documentation & Showcase Artifacts | ⚪ Pending | OpenAPI docs, detailed architecture diagrams, sample analysis reports. |
| **Phase 14** | Final Quality Assurance | ⚪ Pending | End-to-end operational verification, zero-warning build check. |
| **Phase 15** | GitHub Release & Portfolio Preparation | ⚪ Pending | Clean Git history, release tagging, portfolio presentation scripts. |

---

## Detailed Phase Breakdown

### Phase 0: Project Foundation & Hygiene
- [x] Inspect local folder and system environment (Python 3.14, Node.js 24, Git).
- [x] Verify GitHub remote connection (`vyveksharma31/LinkShield`).
- [x] Initialize Git repository with `main` branch.
- [x] Create core documentation files:
  - [x] `BRAIN.md` (Engineering source of truth & ADRs)
  - [x] `README.md` (Professional public project showcase)
  - [x] `ROADMAP.md` (Master phase tracker)
- [x] Establish strict 5-item root rule (`frontend/`, `backend/`, `BRAIN.md`, `README.md`, `ROADMAP.md`).
- [x] Scaffold initial `backend/` and `frontend/` directory structures.

### Phase 1: Architecture & Specifications
- [ ] Define comprehensive REST API schemas (`AnalyzeRequest`, `AnalysisResult`, `Indicator`, `FeatureMetrics`).
- [ ] Formalize URL parsing and normalization pipeline rules.
- [ ] Specify feature extraction matrix (30+ lexical, structural, and information-theoretic features).
- [ ] Define the Hybrid Risk Scoring mathematical formulation.
- [ ] Document explainability rule mapping and threat severity tiers.
- [ ] Update `BRAIN.md` with final architecture specifications.

### Phase 2: Backend Foundation
- [ ] Configure `backend/requirements.txt` with minimal, pinned dependencies.
- [ ] Set up `backend/.gitignore` and `backend/.env.example`.
- [ ] Implement FastAPI application factory in `backend/app/main.py`.
- [ ] Implement CORS middleware, structured JSON logging, and global exception handlers.
- [ ] Implement versioned API routing (`/api/v1/health`, `/api/v1/analyze` scaffold).
- [ ] Write initial Pytest test suite for health and root endpoints.

### Phase 3: URL Analysis & Normalization Engine
- [ ] Build safe URL validator and parser (`backend/app/engine/parser.py`).
- [ ] Implement normalization (scheme defaulting, case folding, Punycode/IDN resolution).
- [ ] Build feature extractor (`backend/app/engine/features.py`) computing:
  - URL length, hostname length, path length, query length.
  - Dot counts, hyphen counts, slash counts, digit ratios.
  - Shannon entropy of hostname and full path.
  - Subdomain depth, suspicious token frequency.
- [ ] Unit test parser and feature extractor with 50+ diverse URLs.

### Phase 4: Security Threat Heuristics
- [ ] Build rule-based indicator engine (`backend/app/engine/heuristics.py`).
- [ ] Implement IP-address host detection (IPv4 literals, hex/octal representations).
- [ ] Implement brand impersonation detection (targeted high-value brand names in subdomains/paths).
- [ ] Implement suspicious TLD lookup (known high-abuse free/cheap TLDs).
- [ ] Implement URL shortener service identification.
- [ ] Implement encoding anomaly detection (excessive `%` hex escapes).

### Phase 5: Dataset & ML Pipeline
- [ ] Curate balanced, clean benchmark dataset of legitimate and phishing URLs.
- [ ] Build reproducible training script (`backend/scripts/train.py`).
- [ ] Train and evaluate candidate models (Random Forest, Logistic Regression).
- [ ] Document metrics (Precision, Recall, F1-Score, False Positive Rate, ROC-AUC).
- [ ] Serialize trained model artifact to `backend/models/`.
- [ ] Implement lightweight inference loader (`backend/app/ml/model_loader.py`).

### Phase 6: Composite Risk Scoring Engine
- [ ] Build risk scoring engine (`backend/app/engine/risk_scorer.py`).
- [ ] Integrate ML prediction probability with heuristic threat weights.
- [ ] Implement critical indicator overrides (guaranteed high floor for egregious flags).
- [ ] Categorize into `LEGITIMATE` (0–25), `SUSPICIOUS` (26–60), and `PHISHING` (61–100).
- [ ] Calibrate overall confidence metrics.

### Phase 7: Explainability & Recommendation Engine
- [ ] Build explainability generator (`backend/app/engine/explainer.py`).
- [ ] Group findings into high-risk indicators and positive security indicators.
- [ ] Generate context-aware recommendations for end users and analysts.
- [ ] Ensure all explanations are grounded in verified evidence.

### Phase 8: Frontend Cyber Dashboard
- [ ] Initialize React + Vite + TypeScript project inside `frontend/`.
- [ ] Set up `frontend/.gitignore` and `frontend/.env.example`.
- [ ] Design custom cyber dark theme design system (`frontend/src/styles/`).
- [ ] Build key components:
  - Header & Status Bar
  - URL Submission Form with quick sample test buttons
  - Risk Gauge & Classification Verdict Card
  - Explanations & Threat Indicators List
  - Extracted URL Features Inspection Grid
  - Recent Analysis History Drawer
- [ ] Validate responsive layout and accessibility.

### Phase 9: Frontend & Backend Integration
- [ ] Implement typed API client (`frontend/src/services/api.ts`).
- [ ] Connect URL analysis form to `POST /api/v1/analyze`.
- [ ] Implement smooth loading, error states, and network fault handling.
- [ ] Verify complete data flow from browser to API, ML, and back.

### Phase 10: Security Hardening & Edge Cases
- [ ] Implement request rate-limiting / size limiting.
- [ ] Guard against hostile ReDoS (Regular Expression Denial of Service).
- [ ] Test extreme URL lengths (e.g., >2048 chars) and illegal Unicode characters.
- [ ] Verify complete absence of external network calls during URL parsing.

### Phase 11: Comprehensive Automated Testing
- [ ] Backend test suite with Pytest covering all modules and edge cases.
- [ ] End-to-end integration tests for the API.
- [ ] Frontend test verification.
- [ ] Achieve high code coverage across core detection components.

### Phase 12: Performance & Latency Optimization
- [ ] Measure end-to-end API response latency (target < 30ms).
- [ ] Ensure single model initialization at startup (FastAPI lifespan).
- [ ] Optimize frontend bundle size and initial load time.

### Phase 13: Documentation & Showcase Artifacts
- [ ] Complete API documentation with curl and Python examples.
- [ ] Provide sample analysis walkthroughs for placement interviews.
- [ ] Update `README.md` and `BRAIN.md` with final metrics.

### Phase 14: Final Quality Assurance
- [ ] Verify clean builds on both frontend and backend.
- [ ] Confirm no orphaned or untracked files in repository root.
- [ ] Perform full manual QA walkthrough.

### Phase 15: GitHub Release & Portfolio Preparation
- [ ] Tag initial production release (`v1.0.0`).
- [ ] Finalize Git commit log.
- [ ] Prepare portfolio summary and resume talking points.
