# 🛡️ LinkShield — Phishing URL Detection & Risk Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.14-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18%2F19-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Security Focus](https://img.shields.io/badge/Security-Defensive%20Static%20Analysis-critical.svg)](#security-principles)

> **LinkShield** is a defense-in-depth cybersecurity platform engineered to detect, classify, and explain phishing and deceptive URLs. By fusing high-dimensional lexical feature extraction, heuristic threat indicators, and calibrated machine learning into an explainable risk scoring engine, LinkShield delivers transparent security intelligence without exposing systems to hostile active web requests.

---

## 📌 Executive Summary

Phishing remains the initial access vector in over 80% of reported cybersecurity breaches. Traditional security measures frequently fall short:
- **Blacklists** suffer from zero-hour latency (malicious domains operate and vanish within minutes).
- **Black-box AI models** output opaque binary decisions without actionable explanations, eroding analyst trust.
- **Unsafe dynamic scanners** risk Server-Side Request Forgery (SSRF), malware infection, and IP reconnaissance when blindly visiting untrusted links.

**LinkShield** solves these challenges by combining **static structural telemetry**, **rule-based domain forensics**, and **explainable machine learning** into an interactive cybersecurity operations dashboard.

---

## 🏛️ System Architecture

```text
                               ┌───────────────────────────┐
                               │   Cybersecurity Client    │
                               │ (React + TypeScript + UI) │
                               └─────────────┬─────────────┘
                                             │ HTTP POST
                                             ▼
                               ┌───────────────────────────┐
                               │    FastAPI REST Engine    │
                               │      (/api/v1/analyze)    │
                               └─────────────┬─────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
         ┌───────────────────────────┐               ┌───────────────────────────┐
         │   Safe URL Normalization  │               │   Lexical Feature Engine  │
         │ - Scheme verification     │               │ - 30+ syntactic features  │
         │ - Punycode translation    │               │ - Shannon entropy metrics │
         │ - Host/Path decomposition │               │ - Token & keyword ratios  │
         └─────────────┬─────────────┘               └─────────────┬─────────────┘
                       │                                           │
                       └─────────────────────┬─────────────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
         ┌───────────────────────────┐               ┌───────────────────────────┐
         │    Security Heuristics    │               │   Machine Learning Core   │
         │ - Brand impersonation     │               │ - Random Forest / LogReg  │
         │ - Obfuscated encodings    │               │ - Calibrated probability  │
         │ - High-risk TLD patterns  │               │ - Vectorized feature feed │
         └─────────────┬─────────────┘               └─────────────┬─────────────┘
                       │                                           │
                       └─────────────────────┬─────────────────────┘
                                             │
                                             ▼
                               ┌───────────────────────────┐
                               │    Composite Risk Engine  │
                               │  - 0–100 Weighted Score   │
                               │  - Multi-tier thresholds  │
                               │  - Explainable indicators │
                               └─────────────┬─────────────┘
                                             │ Structured JSON
                                             ▼
                               ┌───────────────────────────┐
                               │  Tactical Security Report │
                               │  (Verdict, Gauges, Flags) │
                               └───────────────────────────┘
```

---

## 🚀 Key Features

- **⚡ Multi-Layered Threat Detection**: Merges 30+ extracted lexical properties with proven threat heuristics and predictive machine learning.
- **🔍 0–100 Calibrated Risk Scoring**: Eliminates rigid binary labels; provides proportional risk assessment with safety baselines.
- **💡 Explainable Security Findings**: Explicitly details *why* a link was flagged (e.g., suspicious entropy, brand homoglyph, excessive subdomains, or unauthenticated IP host).
- **🛡️ Safe Defensive Static Analysis**: Complete static URL evaluation prevents SSRF, remote exploit triggers, and tracking beacons.
- **🎨 Modern Tactical Dashboard**: High-contrast, dark cybersecurity interface featuring interactive score gauges, indicator breakdowns, and inspection history.
- **🔌 Enterprise REST API**: Clean, versioned endpoints (`/api/v1/analyze`, `/api/v1/health`) with full OpenAPI/Swagger documentation.

---

## 📂 Repository Structure

In accordance with strict architectural invariants, the repository root contains strictly five components:

```text
LinkShield/
│
├── frontend/        # Modern React + Vite + TypeScript web application
├── backend/         # FastAPI REST service, ML pipeline, features, tests
├── BRAIN.md         # Permanent architectural source of truth
├── README.md        # Master documentation and quickstart guide
└── ROADMAP.md       # Incremental phase roadmap and milestone tracker
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18+, TypeScript, Vite, Modern Vanilla CSS / Custom Design Tokens |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, Uvicorn |
| **Machine Learning** | scikit-learn, NumPy, pandas, joblib |
| **Security & Parsing** | `urllib.parse`, `tldextract`, regular expressions, Shannon Entropy algorithms |
| **Testing & QA** | Pytest, HTTPX, ESLint |

---

## ⚡ Quickstart & Local Setup

### Prerequisites
- **Python**: 3.11 or newer (`python --version`)
- **Node.js**: v18.0.0 or newer with npm (`node --version`)
- **Git**: Installed and configured

---

### 1. Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate a Python virtual environment
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```

The API server will launch at `http://127.0.0.1:8000`.  
Explore interactive OpenAPI documentation at `http://127.0.0.1:8000/docs`.

---

### 2. Frontend Setup

```bash
# 1. Open a new terminal and navigate to frontend directory
cd frontend

# 2. Install Node dependencies
npm install

# 3. Launch the Vite development server
npm run dev
```

The cybersecurity operations dashboard will open at `http://localhost:5173`.

---

## 📡 API Reference

### Health Check
```http
GET /api/v1/health
```
**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true
}
```

### URL Analysis
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "url": "https://secure-login.paypal.com.account-update.xyz/verify"
}
```
**Response Preview:**
```json
{
  "url": "https://secure-login.paypal.com.account-update.xyz/verify",
  "verdict": "PHISHING",
  "risk_score": 88,
  "confidence": 0.94,
  "heuristic_flags": [
    {
      "severity": "CRITICAL",
      "category": "Brand Impersonation",
      "description": "Domain mimics PayPal brand inside a subdomain",
      "evidence": "paypal.com in subdomains of account-update.xyz"
    },
    {
      "severity": "HIGH",
      "category": "Suspicious TLD",
      "description": "High-risk generic top-level domain detected (.xyz)",
      "evidence": "xyz"
    }
  ],
  "positive_flags": [
    {
      "category": "Transport Security",
      "description": "Valid HTTPS transport scheme configured"
    }
  ],
  "recommendations": [
    "Do not enter credentials or personal information.",
    "Report this domain to the targeted financial institution's security desk."
  ]
}
```

---

## 🔒 Security Principles

1. **Zero-Trust Input Pipeline**: All URLs submitted are treated as potentially malicious strings. Rigid boundary validation prevents injection attacks and buffer exploitation.
2. **SSRF Immune Architecture**: No automated backend requests are made to user-supplied targets. Evaluation is strictly static, mathematical, and algorithmic.
3. **Graceful Fail-Safe Degradation**: If ML model weights are unavailable or corrupted, the heuristic rule engine guarantees uninterrupted risk assessment.
4. **Zero-Secret Repository Guarantee**: No API keys, credentials, or production tokens are checked into source control.

---

## 👨‍💻 Developer & Attribution

Developed by **Vyvek Sharma**  
*BCA Student specializing in Cybersecurity & Software Development*  
- **GitHub**: [@vyveksharma31](https://github.com/vyveksharma31)  
- **Repository**: [vyveksharma31/LinkShield](https://github.com/vyveksharma31/LinkShield)
