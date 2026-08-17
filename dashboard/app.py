"""
RETAINAI — Customer Retention & LTV Intelligence Platform.

Executive dashboard entry point.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="RETAINAI — Customer Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

from dashboard.components.layout import inject_styles, render_page_header, format_currency
from dashboard.components.cards import render_kpi_card
from dashboard.components.filters import render_sidebar_filters
from dashboard.components.charts import (
    plot_segment_distribution,
    plot_score_distribution,
    plot_business_impact_bar,
    plot_top_revenue_bar,
)
from dashboard.utils.cache import load_global_intelligence_data

inject_styles()


def render_home_dashboard():
    """Render the executive overview dashboard."""
    render_page_header(
        title="Customer Intelligence",
        subtitle="AI-powered overview of churn risk, customer value, and retention opportunities.",
        eyebrow="Overview",
    )

    df_intel = load_global_intelligence_data()

    if df_intel.empty:
        st.warning(
            "Intelligence data is not loaded. Run the scoring pipeline to populate "
            "`reports/customer_intelligence.csv`."
        )
        return

    df_filtered = render_sidebar_filters(df_intel)

    total_cust = len(df_filtered)
    high_risk_cust = len(df_filtered[df_filtered["churn_probability"] >= 0.61])
    avg_churn_prob = df_filtered["churn_probability"].mean() * 100.0 if total_cust > 0 else 0.0
    avg_score = df_filtered["intelligence_score"].mean() if total_cust > 0 else 0.0
    avg_ltv = df_filtered["predicted_ltv"].mean() if total_cust > 0 else 0.0
    revenue_at_risk = (
        df_filtered["churn_probability"].dot(df_filtered["predicted_ltv"])
        if total_cust > 0
        else 0.0
    )
    estimated_retention_savings = (
        df_filtered["estimated_revenue_saved"].sum() if total_cust > 0 else 0.0
    )
    churn_rate = (high_risk_cust / total_cust * 100.0) if total_cust > 0 else 0.0

    row1 = st.columns(5)
    metrics = [
        (f"{total_cust:,}", "Total Customers", "default", None),
        (f"{high_risk_cust:,}", "High-Risk Customers", "danger", "≥ 61% churn probability"),
        (format_currency(revenue_at_risk), "LTV at Risk", "warning", "Probability-weighted exposure"),
        (format_currency(avg_ltv), "Average Customer LTV", "primary", "Predicted lifetime value"),
        (f"{churn_rate:.1f}%", "High-Risk Rate", "danger", f"Avg churn {avg_churn_prob:.1f}%"),
    ]
    for col, (val, label, accent, sub) in zip(row1, metrics):
        with col:
            render_kpi_card(val, label, accent=accent, subtext=sub)

    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

    row2 = st.columns(3)
    with row2[0]:
        render_kpi_card(
            f"{avg_score:.1f}",
            "Average Health Score",
            accent="success",
            subtext="Composite intelligence index (0–100)",
        )
    with row2[1]:
        render_kpi_card(
            format_currency(estimated_retention_savings),
            "Retention Opportunity",
            accent="success",
            subtext="Estimated value from proactive actions",
        )
    with row2[2]:
        render_kpi_card(
            f"{len(df_filtered['customer_segment'].unique())}",
            "Active Segments",
            accent="info",
            subtext="Distinct customer clusters",
        )

    st.divider()

    from dashboard.components.layout import render_section_header

    render_section_header(
        "Portfolio Analytics",
        "Segment distribution, health scores, and retention value across the filtered cohort.",
    )

    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(plot_segment_distribution(df_filtered), use_container_width=True)
        st.plotly_chart(plot_business_impact_bar(df_filtered), use_container_width=True)
    with col_right:
        st.plotly_chart(plot_score_distribution(df_filtered), use_container_width=True)
        st.plotly_chart(plot_top_revenue_bar(df_filtered), use_container_width=True)


if __name__ == "__main__":
    render_home_dashboard()
