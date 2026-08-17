# RETAINAI — AI-Powered Customer Retention & Lifetime Value Intelligence Platform

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38-FF4B4B.svg)](https://streamlit.io/)
[![ROC-AUC Benchmark](https://img.shields.io/badge/Churn_ROC--AUC-0.847-success.svg)](#8-experimental-results--benchmarks)
[![LTV R2](https://img.shields.io/badge/LTV_R2-0.892-success.svg)](#8-experimental-results--benchmarks)
[![Test Suite](https://img.shields.io/badge/PyTest-156%2F156_Passed-brightgreen.svg)](#13-testing)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> **RETAINAI** is an enterprise-grade Customer Retention and Lifetime Value Intelligence Platform designed for subscription businesses and telecommunications providers. It moves beyond traditional binary churn prediction to answer five core business questions: **WHO** will churn, **WHY** they will churn, **WHAT** retention action should be prioritized, **WHICH** intervention offers the best ROI, and **HOW MUCH** revenue is saved under sensitivity simulations.

---

## 📖 Table of Contents

- [1. Project Title](#1-project-title)
- [2. One-Line Description](#2-one-line-description)
- [3. Problem Statement](#3-problem-statement)
- [4. Solution](#4-solution)
- [5. Key Features](#5-key-features)
- [6. Architecture & Data Flow](#6-architecture--data-flow)
- [7. Technology Stack](#7-technology-stack)
- [8. How It Works](#8-how-it-works)
- [9. Dashboard Modules & Visual Demo](#9-dashboard-modules--visual-demo)
- [10. Installation & Setup](#10-installation--setup)
- [11. Environment Variables (`.env.example`)](#11-environment-variables-envexample)
- [12. How to Run](#12-how-to-run)
- [13. Testing & Verification](#13-testing--verification)
- [14. Deployment & Live Demo](#14-deployment--live-demo)
- [15. Project Structure](#15-project-structure)
- [16. Future Improvements](#16-future-improvements)
- [17. License](#17-license)

---

## 1. Project Title

**RETAINAI** — Enterprise Customer Retention & Lifetime Value (LTV) Intelligence Platform

---

## 2. One-Line Description

An end-to-end predictive analytics, SHAP explainability, What-If sensitivity simulation, and Gemini AI decision support platform designed to reduce subscriber churn and maximize customer lifetime value.

---

## 3. Problem Statement

Subscription-based enterprises managing portfolios of thousands of accounts face four major operational challenges:

1. **Reactive Retention**: Outreach occurs only *after* cancellation requests are submitted, when customer churn intent is already finalized.
2. **Black-Box Opacity**: Standard machine learning models output raw scores (e.g., `78% churn probability`) without explaining *why* the subscriber is dissatisfied, preventing tailored interventions.
3. **Capital Misallocation**: Indiscriminate discount campaigns waste retention budgets on low-value accounts or non-at-risk subscribers.
4. **Unquantified Risk**: Management lacks tools to model how contract alterations, price changes, or service additions impact portfolio retention rates prior to live execution.

---

## 4. Solution

**RETAINAI** delivers an integrated, multi-tier intelligence platform that combines gradient boosted machine learning models, Shapley additive attributions, financial simulation engines, and generative AI decision support:

- **Predictive Churn Scoring**: LightGBM binary classifier evaluating subscriber cancellation risk ($0.0 \text{ to } 1.0$) with an optimal decision threshold ($0.610$).
- **LTV Forecasting**: LightGBM regression model estimating 24-month projected lifetime value.
- **SHAP Explainability**: TreeExplainer computing exact positive and negative feature attributions for every prediction.
- **Unsupervised Segmentation**: K-Means clustering ($k=3$) categorizing accounts into High-Value Champions, Loyal Regulars, and Growth Potential segments.
- **What-If Simulator & ROI Optimizer**: Interactive sensitivity tools ranking retention strategies by net retained value and ROI.
- **Gemini AI Copilot**: Contextual conversational assistant generating personalized customer outreach templates with human approval controls.
- **Enterprise MLOps**: FileLock model registry versioning, Population Stability Index (PSI) drift tracking, and 100% automated test coverage.

---

## 5. Key Features

### 📉 Customer Churn Prediction
- **Model**: LightGBM Gradient Boosted Decision Trees trained on 7,045 subscriber records.
- **Metrics**: **ROC-AUC = 0.847**, **F1-Score = 0.633**, Accuracy = 78.1%.
- **Risk Classification Tiers**:
  - **Critical Risk**: $P(\text{Churn}) \ge 0.75$ (1,394 subscribers / 19.8%)
  - **High Risk**: $0.610 \le P(\text{Churn}) < 0.75$ (862 subscribers / 12.2%)
  - **Medium Risk**: $0.350 \le P(\text{Churn}) < 0.610$ (1,200 subscribers / 17.0%)
  - **Monitor / Low Risk**: $P(\text{Churn}) < 0.350$ (3,589 subscribers / 51.0%)

### 💰 LTV Prediction & Revenue Intelligence
- **Model**: LightGBM Regressor ($R^2 = 0.892$, $\text{RMSE} = \$540.20$).
- **Portfolio Valuation**: Reconciles Total LTV at Risk ($\$5.12\text{M}$) and Addressable Retention Opportunity ($\$2.84\text{M}$).
- **High-Value Concentration**: Identifies top accounts (headed by subscriber `9924-JPRMC` at $\text{LTV} = \$8,684.80$).

### 🧩 K-Means Customer Segmentation
- **Segmentation Model**: K-Means ($k=3$) trained on standardized tenure, spend, and service adoption.
- **Persona Clusters**:
  1. **High-Value Champions** (3,079 accounts / 43.7%): High spend ($\$88.50/\text{mo}$), tenure avg 56 mos.
  2. **Loyal Regulars** (2,985 accounts / 42.4%): Moderate spend ($\$62.10/\text{mo}$), tenure avg 32 mos.
  3. **Growth Potential** (981 accounts / 13.9%): Short tenure (6 mos), month-to-month contracts.

### 🔍 SHAP Explainability Engine
- Isolates top feature-level risk drivers (e.g., `Month-to-month contract (+22.0% risk)`, `Fiber optic without Tech Support (+14.5% risk)`).
- Renders waterfall attributions for single-customer transparency.

### 🧪 What-If Financial Risk Simulator
- Allows business users to adjust contract types, monthly discounts, and service add-ons via interactive UI sliders.
- Recalculates churn probability, projected LTV, and net retained revenue in real time.

### 📊 Retention ROI Strategy Optimizer
- Evaluates 4 corporate retention strategies across all 2,256 high-risk accounts.
- Ranks strategies by expected net retained revenue and ROI percentage.

### 🤖 Gemini AI Retention Agent
- Conversational Copilot powered by Google Gemini 1.5 Flash (with fallback to local Ollama and Rule Engine).
- Synthesizes executive briefings, customer risk deep-dives, and follow-up strategy plans.

### ✉️ Personalized Customer Outreach
- Automatically drafts personalized, empathetic retention emails tailored to specific SHAP risk drivers.

### 👤 Human-in-the-Loop Approval Workflow
- Generates campaign drafts and offer structures while requiring explicit account manager approval prior to live execution.

### ⚙️ MLOps & System Observability
- **Model Registry**: FileLock-protected `artifacts/registry/model_registry.json` tracking model versions and promotions.
- **Drift Monitoring**: Population Stability Index (PSI) tracking against training baselines (Warning $\ge 0.10$, Critical $\ge 0.25$).
- **Audit Logging**: Structured JSON Line event logging (`logs/audit.jsonl`).

---

## 6. Architecture & Data Flow

### System Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                              STREAMLIT FRONTEND UI                                |
|   (14 Modular Pages: Executive Overview, Customer 360, Simulator, Operations)    |
+-----------------------------------------+-----------------------------------------+
                                          | HTTP REST (JSON)
                                          v
+-----------------------------------------------------------------------------------+
|                              FASTAPI BACKEND SERVICE                              |
|   (/api/v1/predict, /api/v1/customer/{id}, /api/v1/ai/chat, /api/v1/health)       |
+-------------------+---------------------+-------------------+---------------------+
                    |                     |                   |
                    v                     v                   v
+-----------------------+ +-------------------+ +-----------------------------------+
|   MACHINE LEARNING    | |   AI COPILOT      | |   STORAGE & DATA LAYER            |
| - LightGBM Classifier | | - Gemini 1.5 Flash| | - PostgreSQL Database / CSV       |
| - LightGBM Regressor  | | - Ollama Fallback | | - JSON Model Registry             |
| - K-Means Clustering  | | - Rule Engine     | | - In-Memory LRU Prediction Cache|
| - SHAP TreeExplainer  | +-------------------+ | - Audit Log (logs/audit.jsonl)    |
+-----------------------+                       +-----------------------------------+
```

### End-to-End Data Flow

```
[Customer Data Ingestion]
           │
           ▼
[Validation & Preprocessing] (Pydantic / Pandera / StandardScaler)
           │
           ▼
[Machine Learning Inference] (LightGBM Churn & LTV Models)
           │
           ▼
[Explainable AI Layer] (SHAP TreeExplainer Attributions)
           │
           ▼
[Simulation & Strategy Layer] (What-If Simulator & ROI Optimizer)
           │
           ▼
[AI Copilot Synthesis] (Gemini 1.5 Flash Agent & Email Drafts)
           │
           ▼
[Human Approval & Audit] (Account Manager Approval & Audit Logs)
```

---

## 7. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.12.0 | Core runtime and analytics backend |
| **REST API Server** | FastAPI 0.115.0 | High-performance asynchronous API service |
| **User Interface** | Streamlit 1.38.0 | Interactive multi-page dashboard UI |
| **Database** | PostgreSQL 15.0 / SQLite 3.0 | Persistent relational storage & unit testing DB |
| **ORM / Migration** | SQLAlchemy 2.0.32 / Alembic 1.13.2 | Database object mapping and migrations |
| **Machine Learning** | LightGBM 4.5.0 | Gradient boosted decision tree classifier & regressor |
| **Data Science** | Pandas 2.2.2 / NumPy 1.26.4 / Scikit-Learn 1.4.0 | Data manipulation, scaling, and K-Means |
| **Explainable AI** | SHAP 0.46.0 | Shapley Additive Explanations TreeExplainer |
| **Generative AI** | Google Gemini API / Ollama | Gemini 1.5 Flash conversational agent & fallback |
| **Testing** | PyTest 9.1.1 / PyTest-Cov 7.1.0 | Automated unit testing & coverage reporting |
| **Monitoring** | Prometheus Client 0.20.0 | System health, request metrics, and latency |

---

## 8. How It Works

1. **Ingestion**: Upload CSV files or query PostgreSQL database records.
2. **Preprocessing**: Automatically imputes missing values (`TotalCharges`), scales numeric features, and encodes categorical attributes.
3. **Scoring**: Computes churn probability ($p$) and 24-month projected LTV.
4. **Explanation**: Evaluates SHAP Shapley values to identify specific churn risk drivers.
5. **Simulation**: Adjusts parameters (e.g., converting month-to-month to 1-year contract) and compares Before vs After metrics.
6. **AI Decision Support**: Requests Gemini AI Agent to generate actionable intervention plans and personalized emails.
7. **Execution**: Account manager reviews AI proposals and approves campaign execution.

---

## 9. Dashboard Modules & Visual Demo

The Streamlit dashboard suite includes **14 modular pages**:

1. `1_Executive_Overview.py`: C-Suite portfolio summary, total accounts ($7,045$), high-risk count ($2,256$), LTV at hazard ($\$5.12\text{M}$).
2. `2_Customer_360.py`: Single subscriber search, SHAP waterfall plot, risk drivers, and recommendation card.
3. `3_Churn_Risk_Analyzer.py`: Risk tier filtering and subscriber risk tables.
4. `4_LTV_Intelligence.py`: LTV distribution curves and top 10 revenue accounts.
5. `5_Customer_Segmentation.py`: K-Means 3D scatter plots and segment profiles.
6. `6_What_If_Simulator.py`: Interactive sliders for testing pricing and contract alterations.
7. `7_ROI_Optimizer.py`: Strategy comparison table ranking net revenue saved.
8. `8_AI_Retention_Copilot.py`: Gemini-powered conversational assistant with email generator.
9. `9_Operations.py`: System health, API status, model registry table, and audit logs.
10. `10_Batch_Scoring.py`: CSV bulk file scoring interface.
11. `11_Data_Ingestion.py`: Dataset status and table viewers.
12. `12_Model_Performance.py`: ROC curves, confusion matrix, and calibration charts.
13. `13_Drift_Monitoring.py`: PSI feature drift trends across historical runs.
14. `14_Audit_Logs.py`: Searchable audit event log viewer.

---

## 10. Installation & Setup

### Prerequisites
- Python 3.12.0 or higher
- Git

### Setup Instructions

```bash
# 1. Clone repository
git clone https://github.com/sarafirdose/-Customer-Intelligence-Platform.git
cd Customer-Intelligence-Platform

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 11. Environment Variables (`.env.example`)

Copy `.env.example` to `.env` in the root directory:

```bash
cp .env.example .env
```

### Environment Template Contents

```ini
# Application Environment
ENV=development
DEBUG=true
APP_VERSION=1.0.0

# FastAPI Server Settings
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=dev_secret_key_change_in_production_env

# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=cip_user
DB_PASSWORD=cip_secure_password
DB_NAME=customer_intelligence
DB_SSL_MODE=disable

# Logging & Monitoring
LOG_LEVEL=INFO
LOG_DIR=logs
LOG_FILE_NAME=app.log

# AI Provider Credentials
GEMINI_API_KEY=your_gemini_api_key_here
LLM_PROVIDER=auto
```

---

## 12. How to Run

### Option A: Launch FastAPI Backend Server

```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Documentation (Swagger): `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

### Option B: Launch Streamlit Analytics Dashboard

```bash
streamlit run dashboard/Home.py
```
- Dashboard Access URL: `http://localhost:8501`

---

## 13. Testing & Verification

The repository maintains an automated PyTest suite covering REST API routes, ML models, AI routing, database operations, and data cleaning:

```bash
# Run full automated test suite
pytest -v
```

### Test Suite Results

```
================= 156 passed, 4 warnings in 62.88s (0:01:02) ==================
Total Line Coverage: 63%
```

---

## 14. Deployment & Live Demo

- **Local Execution**: Tested on Windows OS with Python 3.12.0.
- **Docker Support**: Containerized via `Dockerfile` and `docker-compose.yml` deploying FastAPI, PostgreSQL, and Streamlit services.

---

## 15. Project Structure

```
Customer-Intelligence-Platform/
├── artifacts/                  # Trained LightGBM models, scalers, registry
│   ├── models/                 # best_model.pkl, preprocessor.pkl, ltv_model.pkl
│   └── registry/               # model_registry.json & FileLock
├── backend/                    # FastAPI app, ORM models, ML engines, AI agent
│   ├── api/                    # v1 router endpoints (predict, customer, ai, health)
│   ├── core/                   # settings.py, logger.py, metrics.py, scheduler.py
│   ├── database/               # database.py, models.py
│   ├── ml/                     # LightGBM training, SHAP explainer, drift detection
│   └── services/               # ai_agent_engine.py, predict_service.py
├── dashboard/                  # Streamlit frontend UI
│   ├── Home.py                 # Main entry point
│   ├── pages/                  # 14 modular Streamlit pages
│   └── components/             # Reusable UI cards and tables
├── docs/                       # Architectural documentation & recovery guides
├── logs/                       # app.log, audit.jsonl
├── reports/                    # customer_intelligence.csv dataset
├── scripts/                    # Utility scripts (seed_registry.py, run_drift_check.py)
├── tests/                      # 156 PyTest unit and integration tests
├── .env.example                # Environment variables template
├── pyproject.toml              # Dependencies & build configuration
└── README.md                   # Project documentation
```

---

## 16. Future Improvements

1. **Real-Time Event Streaming**: Apache Kafka integration for real-time clickstream event scoring.
2. **Automated Retraining Pipelines**: Triggering LightGBM retraining automatically when PSI drift exceeds $0.25$.
3. **Omnichannel CRM Webhooks**: Pushing approved retention offers directly to Salesforce, HubSpot, and WhatsApp APIs.

---

## 17. License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
