"""
Executive briefing — single-page strategic overview for leadership.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header, format_currency
from dashboard.components.cards import render_kpi_card, render_ai_recommendation
from dashboard.components.charts import apply_chart_style, CHART_COLORS
from dashboard.utils.cache import load_global_intelligence_data

inject_styles()


def render_executive_summary_page() -> None:
    render_page_header(
        title="Executive Summary",
        subtitle="Strategic overview of customer health, churn exposure, revenue risk, and recommended retention actions.",
        eyebrow="Reporting",
    )

    df_intel = load_global_intelligence_data()

    if df_intel.empty:
        st.warning("Intelligence data is not loaded. Metrics cannot be computed.")
        return

    total = len(df_intel)
    high_risk = df_intel[df_intel["churn_probability"] >= 0.61]
    high_risk_count = len(high_risk)
    high_risk_pct = (high_risk_count / total * 100) if total > 0 else 0
    revenue_at_risk = high_risk["churn_probability"].dot(high_risk["predicted_ltv"]) if len(high_risk) > 0 else 0
    total_savings = df_intel["estimated_revenue_saved"].sum()
    avg_score = df_intel["intelligence_score"].mean()
    top_segment = df_intel["customer_segment"].mode().iloc[0] if not df_intel.empty else "—"

    render_section_header("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(f"{total:,}", "Total Customers", accent="primary")
    with col2:
        render_kpi_card(f"{high_risk_count:,} ({high_risk_pct:.1f}%)", "High-Risk Exposure", accent="danger")
    with col3:
        render_kpi_card(format_currency(revenue_at_risk), "LTV at Risk", accent="warning")
    with col4:
        render_kpi_card(format_currency(total_savings), "Retention Opportunity", accent="success")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        render_kpi_card(f"{avg_score:.0f}", "Avg Health Score", accent="info", subtext="0–100 index")
    with col6:
        render_kpi_card("84.7%", "Model ROC-AUC", accent="success", subtext="Churn classifier")
    with col7:
        render_kpi_card(top_segment, "Largest Segment", accent="primary")
    with col8:
        crit_actions = len(df_intel[df_intel["recommendation_priority"] == "Critical"])
        render_kpi_card(f"{crit_actions:,}", "Critical Actions", accent="danger")

    st.divider()

    render_section_header("Major Risks & Opportunities")

    segment_risk = df_intel.groupby("customer_segment").apply(
        lambda g: (g["churn_probability"] * g["predicted_ltv"]).sum()
    ).reset_index()
    segment_risk.columns = ["Segment", "LTV_at_Risk"]
    segment_risk = segment_risk.sort_values("LTV_at_Risk", ascending=False)

    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(
            segment_risk,
            x="Segment",
            y="LTV_at_Risk",
            title="LTV at Risk by Segment",
            color_discrete_sequence=[CHART_COLORS[0]],
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(apply_chart_style(fig1), use_container_width=True)

    with c2:
        if "contract_type" in df_intel.columns:
            contract_risk = df_intel[df_intel["churn_probability"] >= 0.61].groupby("contract_type").size().reset_index(name="Count")
            fig2 = px.pie(
                contract_risk,
                names="contract_type",
                values="Count",
                title="High-Risk Customers by Contract Type",
                color_discrete_sequence=CHART_COLORS,
                hole=0.55,
            )
        else:
            priority_data = df_intel.groupby("recommendation_priority").size().reset_index(name="Count")
            fig2 = px.pie(
                priority_data,
                names="recommendation_priority",
                values="Count",
                title="Actions by Priority Tier",
                color_discrete_sequence=CHART_COLORS,
                hole=0.55,
            )
        st.plotly_chart(apply_chart_style(fig2, height=380), use_container_width=True)

    st.divider()

    render_section_header("Recommended Actions")
    top_actions = df_intel.nlargest(3, "estimated_revenue_saved")
    action_lines = []
    for _, row in top_actions.iterrows():
        action_lines.append(
            f"**{row['customer_segment']}** — {row.get('primary_recommendation', 'Retention outreach')} "
            f"({format_currency(row['estimated_revenue_saved'])} potential value)"
        )
    render_ai_recommendation(
        "Prioritize retention outreach for high-value at-risk segments. "
        + "Top opportunities: "
        + "; ".join(action_lines[:3])
        + ".",
        label="Executive Recommendation",
    )


if __name__ == "__main__":
    render_executive_summary_page()
