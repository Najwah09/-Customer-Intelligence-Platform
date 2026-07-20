"""
Automated Unit Tests for AI Copilot Action Plan Generator.
"""

import pytest
from backend.services.ai_copilot_service import copilot_service


def test_copilot_high_risk_plan():
    """Verify AI Copilot generates critical retention plan for high churn risk."""
    sample = {
        "customer_id": "TEST-CRITICAL-001",
        "churn_probability": 0.85,
        "monthly_charges": 95.00,
        "tenure_months": 3,
        "contract_type": "Month-to-month",
    }
    plan = copilot_service.generate_customer_action_plan(sample)

    assert plan["customer_id"] == "TEST-CRITICAL-001"
    assert plan["risk_level"] == "CRITICAL CHURN RISK"
    assert plan["confidence_score"] > 90.0
    assert "15% Contract Upgrade Discount" in plan["primary_action"]
    assert plan["offer_code"] == "RETENTION-FIBER-15"
    assert plan["estimated_roi_recovery"] > 0
    assert len(plan["action_steps"]) == 3


def test_copilot_low_risk_plan():
    """Verify AI Copilot generates loyalty plan for low churn risk."""
    sample = {
        "customer_id": "TEST-LOYAL-002",
        "churn_probability": 0.10,
        "monthly_charges": 60.00,
        "tenure_months": 48,
        "contract_type": "Two year",
    }
    plan = copilot_service.generate_customer_action_plan(sample)

    assert plan["customer_id"] == "TEST-LOYAL-002"
    assert plan["risk_level"] == "LOW ATTRITION RISK"
    assert "Loyalty Rewards" in plan["primary_action"]
    assert plan["offer_code"] == "LOYALTY-PLUS-500"
