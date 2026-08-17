"""
Comprehensive Automated Unit & Integration Tests for Context-Aware RETAINAI Assistant.

Verifies Section 13 Test Cases:
- TEST 1: High-risk customers -> Why first one risky -> What should I do -> Write a message -> Make it shorter
- TEST 2: What-If Simulator -> Which option is best
- TEST 3: Give me today's report
- TEST 4: What is churn -> How does it work in my project
- TEST 5: Which customers should I contact first -> Why them -> What message should I send
- TEST 6: What is my app -> What architecture does it use -> Why did we use FastAPI
"""

import pytest
from backend.services.ai_agent_engine import AIRetentionAgentEngine, IntentCategory


@pytest.fixture
def agent():
    return AIRetentionAgentEngine()


# -------------------------------------------------------------------
# TEST 1: Customer Multi-Turn Investigation & Action Flow
# -------------------------------------------------------------------
def test_conversation_test_1(agent):
    sid = "test_conv_1"

    t1 = agent.process_natural_language_query("Who are my highest-risk customers?", session_id=sid)
    assert t1["intent"] == IntentCategory.HIGH_RISK_CUSTOMERS.value

    t2 = agent.process_natural_language_query("Why is the first one risky?", session_id=sid)
    assert t2["intent"] == IntentCategory.CUSTOMER_CHURN_REASON.value
    assert "4550-VBOFE" in t2["response"]

    t3 = agent.process_natural_language_query("What should I do?", session_id=sid)
    assert t3["intent"] in [IntentCategory.RETENTION_RECOMMENDATION.value, IntentCategory.ROI_ANALYSIS.value]

    t4 = agent.process_natural_language_query("Write a message.", session_id=sid)
    assert t4["intent"] == IntentCategory.GENERATE_CUSTOMER_MESSAGE.value

    t5 = agent.process_natural_language_query("Make it shorter.", session_id=sid)
    assert t5["intent"] == IntentCategory.REWRITE_MESSAGE.value


# -------------------------------------------------------------------
# TEST 2: What-If Simulator Context & Best Option Resolution
# -------------------------------------------------------------------
def test_conversation_test_2(agent):
    sid = "test_conv_2"

    t1 = agent.process_natural_language_query("What does the What-If Simulator do?", session_id=sid)
    assert t1["intent"] == IntentCategory.SIMULATOR_EXPLANATION.value

    t2 = agent.process_natural_language_query("Which number would be best?", session_id=sid)
    assert t2["intent"] == IntentCategory.SIMULATOR_EXPLANATION.value
    assert "Option 2" in t2["response"] or "Contract Conversion" in t2["response"]


# -------------------------------------------------------------------
# TEST 3: Real Portfolio Today's Report
# -------------------------------------------------------------------
def test_conversation_test_3(agent):
    sid = "test_conv_3"

    t1 = agent.process_natural_language_query("Give me today's report.", session_id=sid)
    assert any(term in t1["response"].lower() for term in ["active customer portfolio", "7,045", "7,043", "subscribers", "portfolio", "churn"])



# -------------------------------------------------------------------
# TEST 4: Conceptual to Project-Specific Grounding
# -------------------------------------------------------------------
def test_conversation_test_4(agent):
    sid = "test_conv_4"

    t1 = agent.process_natural_language_query("What is churn?", session_id=sid)
    assert t1["intent"] == IntentCategory.CONCEPTUAL_CHURN.value

    t2 = agent.process_natural_language_query("How does it work in my project?", session_id=sid)
    assert t2["intent"] == IntentCategory.CONCEPTUAL_CHURN.value
    assert "LightGBM" in t2["response"] or "0.61" in t2["response"]


# -------------------------------------------------------------------
# TEST 5: Contact Prioritization & Outreach Continuity
# -------------------------------------------------------------------
def test_conversation_test_5(agent):
    sid = "test_conv_5"

    t1 = agent.process_natural_language_query("Which customers should I contact first?", session_id=sid)
    assert t1["intent"] == IntentCategory.PRIORITIZE_ACCOUNTS.value

    t2 = agent.process_natural_language_query("Why them?", session_id=sid)
    assert t2["intent"] == IntentCategory.CUSTOMER_CHURN_REASON.value

    t3 = agent.process_natural_language_query("What message should I send?", session_id=sid)
    assert t3["intent"] == IntentCategory.GENERATE_CUSTOMER_MESSAGE.value


# -------------------------------------------------------------------
# TEST 6: Application & Architectural Knowledge Continuity
# -------------------------------------------------------------------
def test_conversation_test_6(agent):
    sid = "test_conv_6"

    t1 = agent.process_natural_language_query("What is my app?", session_id=sid)
    assert t1["intent"] == IntentCategory.APPLICATION_EXPLANATION.value

    t2 = agent.process_natural_language_query("What architecture does it use?", session_id=sid)
    assert t2["intent"] == IntentCategory.ARCHITECTURE.value

    t3 = agent.process_natural_language_query("Why did we use FastAPI?", session_id=sid)
    assert t3["intent"] == IntentCategory.ARCHITECTURE.value
