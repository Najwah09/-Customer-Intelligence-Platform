"""
RETAINAI — Shared Layout Utilities & Sidebar Branding.
"""

import html
from pathlib import Path
from typing import Optional, Tuple
import streamlit as st

_ASSETS = Path(__file__).resolve().parents[1] / "assets" / "styles.css"


def inject_styles() -> None:
    """Inject global CSS design system."""
    if _ASSETS.exists():
        with open(_ASSETS, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def format_currency(val: float) -> str:
    """Format numeric float as clean USD currency string."""
    try:
        val = float(val)
        if abs(val) >= 1_000_000:
            return f"${val / 1_000_000:,.2f}M"
        elif abs(val) >= 1_000:
            return f"${val / 1_000:,.1f}K"
        return f"${val:,.2f}"
    except Exception:
        return "$0.00"


def risk_level_label(prob: float) -> Tuple[str, str]:
    """Return risk level label and badge color token for churn probability."""
    try:
        prob = float(prob)
        if prob >= 0.61:
            return "High", "danger"
        elif prob >= 0.40:
            return "Medium", "warning"
        return "Low", "success"
    except Exception:
        return "Unknown", "neutral"


def render_risk_badge(prob: float) -> None:
    """Render semantic risk badge widget using single-line HTML."""
    label, badge_type = risk_level_label(prob)
    safe_label = html.escape(f"{label} Risk ({prob*100:.1f}%)")
    badge_html = f'<span class="retainai-badge retainai-badge-{badge_type}">{safe_label}</span>'
    st.markdown(badge_html, unsafe_allow_html=True)


def render_page_header(
    title: str,
    subtitle: str,
    eyebrow: Optional[str] = None,
) -> None:
    """Render a clean, restrained page title block using single-line HTML."""
    raw_title = title.replace("🔮", "").replace("👑", "").replace("🕵️", "").replace("💬", "").replace("⚡", "").replace("📊", "").replace("🏆", "").replace("⚙️", "").replace("📂", "").replace("🧪", "").replace("💰", "").replace("🏥", "").replace("🔄", "").strip()
    safe_title = html.escape(raw_title)
    safe_subtitle = html.escape(str(subtitle))

    badge_html = f'<span class="retainai-badge retainai-badge-neutral">{html.escape(str(eyebrow))}</span>' if eyebrow else ""
    header_html = f'<div class="retainai-header-banner"><div><h1 class="retainai-header-title">{safe_title}</h1><p class="retainai-header-subtitle">{safe_subtitle}</p></div><div>{badge_html}</div></div>'
    st.markdown(header_html, unsafe_allow_html=True)


def render_sidebar_branding() -> None:
    """Render minimalist sidebar header branding."""
    brand_html = f'<div style="padding: 12px 0 20px 0; border-bottom: 1px solid var(--border); margin-bottom: 16px;"><div style="font-size: 16px; font-weight: 700; letter-spacing: -0.02em; color: var(--text-primary);">RETAINAI</div><div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">Retention Intelligence Engine</div></div>'
    st.sidebar.markdown(brand_html, unsafe_allow_html=True)


def render_section_header(title: str, description: Optional[str] = None) -> None:
    """Render a section heading with optional description."""
    safe_title = html.escape(str(title))
    desc_html = f'<p style="font-size: 13px; color: var(--text-secondary); margin-top: 2px;">{html.escape(str(description))}</p>' if description else ""
    section_html = f'<div style="margin-top: 24px; margin-bottom: 12px;"><h2 style="font-size: 16px; font-weight: 600; color: var(--text-primary); margin: 0;">{safe_title}</h2>{desc_html}</div>'
    st.markdown(section_html, unsafe_allow_html=True)


def render_empty_state(title: str, description: str) -> None:
    """Render a professional empty state panel using single-line HTML."""
    safe_title = html.escape(str(title))
    safe_desc = html.escape(str(description))
    empty_html = f'<div class="retainai-card" style="text-align: center; padding: 40px 24px;"><div style="font-size: 15px; font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">{safe_title}</div><div style="font-size: 13px; color: var(--text-secondary); max-width: 400px; margin: 0 auto;">{safe_desc}</div></div>'
    st.markdown(empty_html, unsafe_allow_html=True)
