"""
Churn intelligence — risk analytics and high-risk watchlist.
"""

from pathlib import Path

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header
from dashboard.components.cards import render_kpi_card
from dashboard.components.filters import render_sidebar_filters
from dashboard.components.tables import render_interactive_table
from dashboard.utils.cache import load_global_intelligence_data

inject_styles()

BASE_DIR = Path(__file__).resolve().parents[2]
PLOT_DIR = BASE_DIR / "reports" / "plots"


def render_churn_page():
    render_page_header(
        title="Churn Intelligence",
        subtitle="Monitor churn risk across the portfolio, review model performance, and manage the high-risk watchlist.",
        eyebrow="Customer Intelligence",
    )

    df_intel = load_global_intelligence_data()
    if df_intel.empty:
        st.error("Analytics data is not loaded.")
        return

    df_filtered = render_sidebar_filters(df_intel)

    high_risk_df = df_filtered[df_filtered["churn_probability"] >= 0.61].sort_values(
        by="churn_probability", ascending=False
    )
    med_risk_df = df_filtered[
        (df_filtered["churn_probability"] >= 0.40) & (df_filtered["churn_probability"] < 0.61)
    ]
    avg_risk = df_filtered["churn_probability"].mean() * 100.0 if not df_filtered.empty else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(f"{len(high_risk_df):,}", "High-Risk Watchlist", accent="danger", subtext="≥ 61% probability")
    with c2:
        render_kpi_card(f"{len(med_risk_df):,}", "Medium Risk", accent="warning", subtext="40–61% range")
    with c3:
        render_kpi_card(f"{avg_risk:.1f}%", "Cohort Mean Risk", accent="primary")
    with c4:
        render_kpi_card("0.847", "Model ROC-AUC", accent="success", subtext="Production classifier")

    st.divider()

    render_section_header(
        "Churn Watchlist",
        "Customers exceeding the high-risk threshold, sorted by churn probability.",
    )

    watchlist_cols = [
        "customer_id", "churn_probability", "customer_segment", "rfm_persona",
        "intelligence_score", "primary_recommendation", "recommendation_priority",
    ]
    render_interactive_table(high_risk_df[watchlist_cols], page_size=15, key="watchlist")

    st.divider()

    render_section_header(
        "Model Performance",
        "Classifier evaluation curves from the latest training run.",
    )
    col_roc, col_pr = st.columns(2)
    with col_roc:
        roc_path = PLOT_DIR / "roc_curve.png"
        if roc_path.exists():
            st.image(str(roc_path), caption="ROC Curve")
        else:
            st.info("ROC curve not available. Run `scripts/train_all.py` to generate evaluation plots.")

    with col_pr:
        pr_path = PLOT_DIR / "pr_curve.png"
        if pr_path.exists():
            st.image(str(pr_path), caption="Precision-Recall Curve")
        else:
            st.info("PR curve not available.")

    col_cal, col_cm = st.columns(2)
    with col_cal:
        cal_path = PLOT_DIR / "calibration_curve.png"
        if cal_path.exists():
            st.image(str(cal_path), caption="Calibration Curve")
    with col_cm:
        cm_path = PLOT_DIR / "confusion_matrix.png"
        if cm_path.exists():
            st.image(str(cm_path), caption="Confusion Matrix (threshold 0.61)")


if __name__ == "__main__":
    render_churn_page()
