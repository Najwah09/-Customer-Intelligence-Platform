"""
RETAINAI — Enterprise Card Components & Recommendation Panels.

Clean, restrained, professional metric cards, headers, and analytical callouts.
"""

import html
from typing import Any, Dict, List, Optional, Tuple
import streamlit as st


def render_kpi_card(
    value: str,
    label: str,
    accent: str = "default",
    trend: Optional[str] = None,
    trend_type: str = "neutral",
    subtext: Optional[str] = None,
    border_color: Optional[str] = None,
):
    """
    Render a clean, restrained enterprise metric card.
    Single-line HTML construction prevents Streamlit markdown code block escaping bugs.
    """
    raw_label = label.replace("🔮", "").replace("👑", "").replace("🕵️", "").replace("💬", "").strip()
    safe_label = html.escape(raw_label)
    safe_value = html.escape(str(value))

    badge_html = ""
    if trend:
        badge_type = "neutral"
        if trend_type == "positive":
            badge_type = "success"
        elif trend_type == "negative":
            badge_type = "danger"
        elif trend_type == "warning":
            badge_type = "warning"
        safe_trend = html.escape(str(trend))
        badge_html = f'<span class="retainai-badge retainai-badge-{badge_type}">{safe_trend}</span>'

    subtext_html = f'<div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">{html.escape(str(subtext))}</div>' if subtext else ""

    card_html = f'<div class="retainai-card"><div class="retainai-card-header"><span class="retainai-card-title">{safe_label}</span>{badge_html}</div><div class="retainai-card-value">{safe_value}</div>{subtext_html}</div>'
    st.markdown(card_html, unsafe_allow_html=True)


def render_executive_header(
    title: str,
    subtitle: str,
    badge_text: Optional[str] = None,
    status_online: bool = True,
):
    """Render crisp page title banner using clean single-line HTML."""
    raw_title = title.replace("🔮", "").replace("👑", "").replace("🕵️", "").replace("💬", "").replace("⚡", "").replace("📊", "").replace("🏆", "").replace("⚙️", "").replace("📂", "").replace("🧪", "").replace("💰", "").replace("🏥", "").replace("🔄", "").strip()
    safe_title = html.escape(raw_title)
    safe_subtitle = html.escape(str(subtitle))

    badge_html = f'<span class="retainai-badge retainai-badge-neutral">{html.escape(str(badge_text))}</span>' if badge_text else ""

    banner_html = f'<div class="retainai-header-banner"><div><h1 class="retainai-header-title">{safe_title}</h1><p class="retainai-header-subtitle">{safe_subtitle}</p></div><div>{badge_html}</div></div>'
    st.markdown(banner_html, unsafe_allow_html=True)


def render_ai_recommendation(text: str, label: str = "AI Recommendation") -> None:
    """Render a clean AI recommendation panel."""
    safe_label = html.escape(str(label))
    safe_text = html.escape(str(text))
    panel_html = f'<div class="retainai-ai-panel"><div class="retainai-ai-panel-title">{safe_label}</div><p class="retainai-ai-panel-text">{safe_text}</p></div>'
    st.markdown(panel_html, unsafe_allow_html=True)


def render_metric_panel(title: str, rows: List[Tuple[str, str]]) -> None:
    """Render a key-value metric panel."""
    safe_title = html.escape(str(title))
    rows_html = "".join(
        f'<div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid var(--border); font-size: 13px;"><span style="color: var(--text-secondary);">{html.escape(str(k))}</span><span style="font-weight: 500; color: var(--text-primary);">{html.escape(str(v))}</span></div>'
        for k, v in rows
    )
    panel_html = f'<div class="retainai-card"><div class="retainai-card-title" style="margin-bottom: 12px;">{safe_title}</div>{rows_html}</div>'
    st.markdown(panel_html, unsafe_allow_html=True)


def render_strategy_recommendation(reasoning: str) -> None:
    """Render a recommended strategy callout."""
    render_ai_recommendation(text=reasoning, label="Recommended Retention Strategy")


def render_ai_copilot_widget(
    query: str = "",
    response: str = "",
    confidence: float = 0.0,
):
    """Legacy wrapper — renders clean recommendation panel."""
    if response:
        render_ai_recommendation(response, label="Portfolio Intelligence Summary")


render_ai_assistant_card = render_ai_recommendation
