# RETAINAI — REST API Documentation

> **Base URL**: `http://localhost:8000/api/v1`  
> **OpenAPI Swagger**: `http://localhost:8000/docs`  

---

## 🤖 1. AI-Native Intelligence Endpoints

### A. Natural Language AI Analyst Chat
- **Endpoint**: `POST /api/v1/ai/chat`
- **Request Body**:
  ```json
  {
    "query": "Which high-value customers are most likely to churn?",
    "session_id": "session_102"
  }
  ```
- **Response**:
  ```json
  {
    "query": "Which high-value customers are most likely to churn?",
    "response": "Identified 5 high-risk subscriber accounts with churn probability >= 61.0%...",
    "data": [...],
    "invoked_tools": ["search_customers"],
    "grounding_status": "VERIFIED_TOOL_DATA"
  }
  ```

---

### B. AI Customer 360 View
- **Endpoint**: `GET /api/v1/ai/customer-360/{customer_id}`
- **Response**:
  ```json
  {
    "customer_id": "0003-MKNFE",
    "response": "### 🤖 AI Customer 360: Account #0003-MKNFE...",
    "customer_profile": {...},
    "shap_explanation": {...},
    "roi_analysis": {...},
    "retention_plan": {...}
  }
  ```

---

### C. What-If Intervention Simulator
- **Endpoint**: `POST /api/v1/ai/simulation/intervention`
- **Request Body**:
  ```json
  {
    "customer_id": "0003-MKNFE",
    "modified_parameters": {
      "contract_type": "Two year",
      "monthly_charges": 60.0,
      "tech_support": "Yes"
    }
  }
  ```
- **Response**:
  ```json
  {
    "customer_id": "0003-MKNFE",
    "disclaimer": "MODEL-BASED SIMULATION: Calculated from machine learning sensitivity curves...",
    "before": {"churn_probability": 0.65, "predicted_ltv": 2400.0},
    "after": {"churn_probability": 0.28, "predicted_ltv": 2880.0},
    "difference": {"churn_reduction": 0.37, "potential_value_saved": 1065.60}
  }
  ```

---

### D. Retention ROI Optimizer
- **Endpoint**: `POST /api/v1/ai/retention/roi`
- **Request Body**:
  ```json
  {"customer_id": "0003-MKNFE"}
  ```
- **Response**:
  ```json
  {
    "customer_id": "0003-MKNFE",
    "recommended_strategy": "Strategy B: Priority VIP Tech Support",
    "recommendation_reasoning": "Strategy B is recommended because it yields the highest expected net value...",
    "ranked_strategies": [...]
  }
  ```

---

### E. Executive AI Briefing
- **Endpoint**: `GET /api/v1/ai/executive/briefing`
- **Response**:
  ```json
  {
    "total_subscribers": 7043,
    "high_risk_subscribers": 2255,
    "total_ltv_at_risk": 1824500.0,
    "executive_summary": "### 👑 TODAY'S AI EXECUTIVE BUSINESS BRIEFING..."
  }
  ```

---

### F. AI Safety Audit Log
- **Endpoint**: `GET /api/v1/ai/audit`
- **Response**:
  ```json
  {
    "status": "VERIFIED_GROUNDED_ARCHITECTURE",
    "hallucination_control": "ACTIVE",
    "verified_tool_calls_count": 142
  }
  ```
