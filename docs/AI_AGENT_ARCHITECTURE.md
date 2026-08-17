# RETAINAI — AI Agent & Tool Architecture Specification

> **Platform**: RETAINAI (AI-Powered Customer Retention & Lifetime Value Intelligence Platform)  
> **Module**: Agentic Orchestration & Grounded Tool Architecture  

---

## 🤖 1. Architectural Overview

```
                                 USER INTERFACE LAYER
                       (Streamlit / REST Clients / Natural Language)
                                         |
                                         v
                         +-------------------------------+
                         |   AI RETENTION AGENT ENGINE   |
                         | (backend/services/ai_agent.py)|
                         +---------------+---------------+
                                         |
                                         v
                         +-------------------------------+
                         |     STRUCTURED TOOL LAYER     |
                         | (backend/services/ai_tools.py)|
                         +---------------+---------------+
                                         |
      +-------------------+--------------+--------------+-------------------+
      |                   |                             |                   |
      v                   v                             v                   v
+-----------+    +------------------+         +-----------+       +-------------------+
| PostgreSQL|    | ML Prediction    |         | SHAP Engine|       | Simulation / ROI  |
| Database  |    | (Churn & LTV)    |         | (Explain) |       | Optimizer Engine  |
+-----------+    +------------------+         +-----------+       +-------------------+
```

---

## 🛠️ 2. Verified Tool Suite (`backend/services/ai_tools.py`)

The AI Retention Agent executes factual queries exclusively through the 10 verified tools below:

| Tool Method Name | Input Parameters | Return Output Payload | Business Purpose |
|---|---|---|---|
| `get_customer()` | `customer_id: str` | Subscriber profile dictionary | Fetches single subscriber record from database. |
| `search_customers()` | `min_churn_prob`, `segment`, `limit` | List of subscriber records | Searches portfolio for targeted cohorts. |
| `predict_churn()` | `customer_data: Dict` | `churn_probability`, `risk_level` | Runs LightGBM classification inference. |
| `predict_ltv()` | `customer_data: Dict` | `predicted_ltv`, `remaining_months` | Runs LightGBM regression inference. |
| `get_customer_segment()` | `customer_data: Dict` | `customer_segment`, `rfm_persona` | Maps subscriber to 4 K-Means cohorts. |
| `get_shap_explanation()` | `customer_id: str` | Waterfall & top driver list | Computes SHAP feature importance attributions. |
| `calculate_value_at_risk()`| `customer_data: Dict` | `value_at_risk`, `annual_at_risk` | Quantifies financial dollar exposure. |
| `simulate_intervention()` | `customer_id`, `modified_params` | BEFORE vs AFTER risk metrics | Runs model-driven what-if sensitivity curves. |
| `calculate_retention_roi()`| `customer_id: str` | Strategy ranking list & Net ROI | Ranks 4 retention strategies by net value. |
| `generate_retention_plan()` | `customer_id: str` | Priority, actions, CS template | Generates personalized action plan script. |

---

## 🛡️ 3. Hallucination Control & Safety Guardrails

To prevent LLM hallucination and ungrounded statements:
1. **Tool Grounding**: The AI Retention Agent never invents numerical predictions or customer spend values; all numbers are retrieved directly from tool execution outputs.
2. **Disclaimer Transparency**: All What-If simulations include explicit disclaimers: *"MODEL-BASED SIMULATION: Calculated from machine learning sensitivity curves, not guaranteed real-world outcomes."*
3. **Audit Logging**: Every AI query, tool invocation chain, and grounding status is recorded in `AIAuditLog` and accessible via `GET /api/v1/ai/audit`.
