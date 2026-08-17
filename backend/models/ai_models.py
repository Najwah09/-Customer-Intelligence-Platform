"""
SQLAlchemy ORM models for AI-native extensions in RETAINAI platform.

Includes schemas for AI conversations, messages, retention recommendations,
intervention simulations, ROI optimization results, and AI safety audit logs.
"""

from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.models.customer import Base


class AIConversation(Base):
    """Stores natural language chat sessions."""

    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), default="New Retention Chat")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    messages = relationship(
        "AIMessage", back_populates="conversation", cascade="all, delete-orphan"
    )


class AIMessage(Base):
    """Stores individual messages within a conversation session."""

    __tablename__ = "ai_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(
        Integer, ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(String(20), nullable=False)  # user, assistant, system, tool
    content = Column(Text, nullable=False)
    tool_calls_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    conversation = relationship("AIConversation", back_populates="messages")


class RetentionRecommendation(Base):
    """Stores generated AI retention recommendations per customer."""

    __tablename__ = "retention_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True, nullable=False)
    primary_action = Column(String(255), nullable=False)
    offer_code = Column(String(50), nullable=False)
    estimated_roi = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    action_steps_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class InterventionSimulation(Base):
    """Stores model-driven what-if simulation scenarios."""

    __tablename__ = "intervention_simulations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True, nullable=False)
    before_churn_probability = Column(Float, nullable=False)
    after_churn_probability = Column(Float, nullable=False)
    churn_reduction = Column(Float, nullable=False)
    before_ltv = Column(Float, nullable=False)
    after_ltv = Column(Float, nullable=False)
    value_saved = Column(Float, nullable=False)
    modified_parameters = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ROIAnalysis(Base):
    """Stores comparative retention strategy ROI rankings."""

    __tablename__ = "roi_analysis"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True, nullable=False)
    recommended_strategy = Column(String(100), nullable=False)
    strategies_json = Column(JSON, nullable=False)
    assumptions_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AIAuditLog(Base):
    """Audit log for AI tool grounding and safety verification."""

    __tablename__ = "ai_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(100), nullable=False)
    prompt_hash = Column(String(64), nullable=False)
    tools_invoked = Column(JSON, nullable=False)
    grounding_verified = Column(String(20), default="VERIFIED")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
