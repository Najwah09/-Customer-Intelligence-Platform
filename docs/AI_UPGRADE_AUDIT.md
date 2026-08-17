# RETAINAI — Pre-Upgrade Architecture Audit Report

> **Target Platform**: RETAINAI (AI-Powered Customer Retention & Lifetime Value Intelligence Platform)  
> **Audit Date**: 2026-08-11  
> **Status**: Audit Completed — Baseline System Analyzed  

---

## 🛠️ 1. Comprehensive System Inspection

### A. Data Ingestion & Storage Architecture
- **Database Layer (`backend/database/`, `backend/models/`)**: PostgreSQL with SQLAlchemy ORM models (`Customer`, `Contract`, `Service`, `Billing`, `Prediction`, `ImportHistory`).
- **Automated Ingestion Engine (`backend/services/auto_ingestion.py`)**: CSV watch folder scanner (`data/incoming/`), incremental PostgreSQL auto-sync, and REST API endpoints (`/api/v1/ingest/record`, `/ingest/batch`).
- **Data Validation (`backend/ml/validation.py`)**: Pandera data validation schema for telecom subscriber columns.

### B. Machine Learning Pipeline (`backend/ml/`)
- **Churn Classifier (`backend/ml/training.py`, `artifacts/models/best_model.pkl`)**: Benchmark trained LightGBM & XGBoost models (**ROC-AUC: 0.847**, Optimal Threshold: `0.61`).
- **LTV Forecast Regressor (`backend/ml/training.py`, `artifacts/models/ltv_model.pkl`)**: LightGBM Regressor for projected lifetime revenue (**\(R^2\): 0.9987**, MAE: `$56.14`).
- **Customer Segmentation (`backend/ml/intelligence.py`)**: K-Means clustering (4 cohorts: High-Value, Loyal, Growth, Budget) and RFM behavioral personas.
- **Explainability (`backend/ml/explain.py`)**: SHAP TreeExplainer for global feature importance and individual subscriber force attributions.

### C. Backend API & Observability (`backend/api/`)
- **FastAPI Core (`backend/api/main.py`)**: Endpoints for customer intelligence (`/customer/{id}`), churn prediction (`/predict/churn`), batch scoring (`/customers/batch_intelligence`), AI recommendations (`/copilot/recommend`), metrics (`/metrics`), health (`/health`), and model registry status (`/observability/registry`).
- **Observability (`backend/core/`)**: Structured JSON logging, append-only audit trail (`logs/audit.jsonl`), Population Stability Index (PSI) drift monitoring (`backend/ml/drift.py`), and 6 background tasks managed by APScheduler (`backend/core/scheduler.py`).

### D. Frontend Dashboard (`dashboard/`)
- **Streamlit Enterprise UI**: 11 multi-page views with Apple/Stripe-inspired glassmorphism theme, Plotly charts, AI Copilot panel, and subscriber watchlists.

---

## 🔍 2. Audit Findings & Upgrade Gap Analysis

| System Component | Current Baseline State | RETAINAI Upgrade Target | Gap / Required Enhancement |
|---|---|---|---|
| **AI Intelligence Layer** | Basic rules-based Copilot recommendation snippet | **Full Agentic AI Engine & Natural Language Analyst** | Implement `AIAgentEngine` with tool-grounding, local/API LLM router, and hallucination control. |
| **Tool Execution Layer** | Ad-hoc service calls | **Structured Tool Layer** | Create 10 dedicated AI tools (`get_customer`, `search_customers`, `predict_churn`, `predict_ltv`, `get_customer_segment`, `get_shap_explanation`, `calculate_value_at_risk`, `simulate_intervention`, `calculate_retention_roi`, `generate_retention_plan`). |
| **Database Schema** | Basic customer metadata & predictions | **AI-Native Extension Tables** | Add `ai_conversations`, `ai_messages`, `retention_recommendations`, `intervention_simulations`, `roi_analysis`, and `ai_audit_logs`. |
| **What-If Simulation** | Static what-if UI placeholders | **Model-Driven What-If Intervention Simulator** | Build `InterventionSimulator` engine calculating BEFORE vs AFTER metrics for contract, price, discount, and tenure adjustments. |
| **ROI Optimization** | Static ROI metric cards | **Strategy Comparison & Ranking Engine** | Build `ROIOptimizer` evaluating 4 retention strategies (Discount, Premium Support, Annual Conversion, No Action) with net value ranking. |
| **Natural Language Analyst** | Standard filter dropdowns | **Interactive Natural Language AI Analyst Chat** | Add a conversational AI chat interface in dashboard with real DB query grounding and tool invocation. |
| **Executive Intelligence** | Static card metrics | **AI Executive Briefing Engine** | Build automated natural-language executive briefings generated dynamically from current DB and model states. |
| **AI Security & Grounding** | Standard input strings | **Strict Grounded-Response Guardrails** | Implement prompt injection defense, factual DB/ML tool verification, and hallucination prevention rules. |

---

## 🎯 3. Upgrade Strategy & Guarantees

1. **Non-Breaking Extension**: All 134 existing tests, FastAPI endpoints, Streamlit pages, and background scheduler jobs will be preserved and extended.
2. **Zero Mandatory Paid API Dependency**: The system will feature a rule-grounded local AI engine with optional API provider fallback (OpenAI/Ollama/Anthropic configurable via `.env`).
3. **Strict AI Safety**: The AI layer will never hallucinate customer records, SHAP values, or predictions; all facts will be retrieved through verified tool calls.
