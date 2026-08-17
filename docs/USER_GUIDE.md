# RETAINAI — User Guide & Operator Walkthrough

> **Platform**: RETAINAI (AI-Powered Customer Retention & Lifetime Value Intelligence Platform)  
> **UI Dashboard**: `http://localhost:8501`  
> **Backend REST APIs**: `http://localhost:8000/docs`  

---

## 🚀 1. Quickstart Guide

### Start FastAPI Backend Engine:
```bash
# Activate virtual environment
venv/Scripts/activate

# Launch FastAPI service
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

### Start Streamlit Master Dashboard:
```bash
# Launch Streamlit frontend
streamlit run dashboard/app.py --server.port 8501
```

---

## 📱 2. Dashboard Navigation Walkthrough

1. **👑 Executive AI Briefing (`11_Executive_Summary.py`)**: Single-page C-suite overview summarizing portfolio health, high-risk account volumes, annual LTV exposure, and recommended retention strategies.
2. **🕵️ AI Customer 360 (`2_Customers.py`)**: Single-subscriber lookup engine showing live churn risk, predicted LTV, SHAP force plot attributions, and AI retention action plans.
3. **💬 AI Retention Agent & Natural Language Analyst (`12_AI_Retention_Agent.py`)**: Conversational chat interface to ask natural language questions (e.g., *"Which high-value accounts are at risk?"*) and inspect grounded tool responses.
4. **🧪 What-If Intervention Simulator (`13_What_If_Simulator.py`)**: Interactive sensitivity simulator where managers adjust contract types, pricing, and tech support to observe model-driven BEFORE vs AFTER risk shifts.
5. **💰 Retention ROI Strategy Optimizer (`14_Retention_ROI_Optimizer.py`)**: Evaluates 4 retention strategies (Discount, VIP Support, Annual Plan, No Action) ranked by expected net value and ROI percentage.
6. **📂 AI Reports Center (`8_Reports.py`)**: View and download executive briefings, model evaluations, and CSV/markdown intelligence exports.
7. **⚙️ Operations & Telemetry (`9_Operations.py`)**: System liveness monitoring, model registry status, and PSI feature drift tracking.
