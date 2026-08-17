"""
Unit and Integration Test Suite for RETAINAI AI Engine, Tools, and REST Endpoints.

Verifies AI Tool Layer, Natural Language AI Analyst, What-If Simulator,
Retention ROI Optimizer, AI Safety Grounding, and REST APIs.
"""

import pytest
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.services.ai_tools import ai_tools
from backend.services.ai_agent_engine import ai_agent

client = TestClient(app)


# -------------------------------------------------------------------
# 1. AI Tool Layer Unit Tests
# -------------------------------------------------------------------

def test_ai_tools_get_customer():
    res = ai_tools.get_customer("0003-MKNFE")
    assert isinstance(res, dict)
    assert "customer_id" in res or "error" in res


def test_ai_tools_predict_churn():
    sample = {
        "customer_id": "TEST-001",
        "tenure_months": 3,
        "monthly_charges": 95.0,
        "contract_type": "Month-to-month",
        "total_charges": 285.0,
    }
    res = ai_tools.predict_churn(sample)
    assert "churn_probability" in res
    assert 0.0 <= res["churn_probability"] <= 1.0
    assert res["risk_level"] in ["CRITICAL", "ELEVATED", "LOW"]


def test_ai_tools_predict_ltv():
    sample = {
        "customer_id": "TEST-001",
        "monthly_charges": 70.0,
        "tenure_months": 12,
        "total_charges": 840.0,
        "churn_probability": 0.20,
    }
    res = ai_tools.predict_ltv(sample)
    assert "predicted_ltv" in res
    assert res["predicted_ltv"] >= 840.0


def test_ai_tools_simulate_intervention():
    modified = {"contract_type": "Two year", "monthly_charges": 60.0}
    res = ai_tools.simulate_intervention("0003-MKNFE", modified)
    assert "before" in res
    assert "after" in res
    assert "difference" in res
    assert "disclaimer" in res
    assert "MODEL-BASED SIMULATION" in res["disclaimer"]


def test_ai_tools_calculate_retention_roi():
    res = ai_tools.calculate_retention_roi("0003-MKNFE")
    assert "recommended_strategy" in res
    assert "ranked_strategies" in res
    assert len(res["ranked_strategies"]) == 4


def test_ai_tools_generate_retention_plan():
    res = ai_tools.generate_retention_plan("0003-MKNFE")
    assert "priority" in res
    assert "recommended_actions" in res
    assert "customer_service_message_template" in res


# -------------------------------------------------------------------
# 2. AI Retention Agent Unit Tests
# -------------------------------------------------------------------

def test_ai_agent_process_query_churn():
    res = ai_agent.process_natural_language_query("Which customers are most likely to churn?")
    assert "response" in res
    assert res["grounding_status"] == "VERIFIED_TOOL_DATA"
    assert len(res["invoked_tools"]) > 0


def test_ai_agent_process_query_high_value():
    res = ai_agent.process_natural_language_query("Show me high-value customers at risk.")
    assert "response" in res
    assert res["grounding_status"] == "VERIFIED_TOOL_DATA"


def test_ai_agent_executive_briefing():
    res = ai_agent.generate_executive_briefing()
    assert "executive_summary" in res
    assert "total_subscribers" in res
    assert "high_risk_subscribers" in res


# -------------------------------------------------------------------
# 3. REST API Endpoint Integration Tests
# -------------------------------------------------------------------

def test_api_ai_chat():
    payload = {"query": "Which customers are most likely to churn?"}
    response = client.post("/api/v1/ai/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "grounding_status" in data


def test_api_customer_360_intelligence():
    response = client.get("/api/v1/ai/customer-360/0003-MKNFE")
    assert response.status_code == 200
    data = response.json()
    assert "customer_profile" in data or "customer_id" in data


def test_api_retention_recommend():
    payload = {"customer_id": "0003-MKNFE"}
    response = client.post("/api/v1/ai/retention/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_actions" in data


def test_api_simulation_intervention():
    payload = {
        "customer_id": "0003-MKNFE",
        "modified_parameters": {"contract_type": "Two year"}
    }
    response = client.post("/api/v1/ai/simulation/intervention", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "before" in data
    assert "after" in data


def test_api_retention_roi():
    payload = {"customer_id": "0003-MKNFE"}
    response = client.post("/api/v1/ai/retention/roi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ranked_strategies" in data


def test_api_executive_briefing():
    response = client.get("/api/v1/ai/executive/briefing")
    assert response.status_code == 200
    data = response.json()
    assert "executive_summary" in data



def test_api_ai_audit():
    response = client.get("/api/v1/ai/audit")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "VERIFIED_GROUNDED_ARCHITECTURE"
