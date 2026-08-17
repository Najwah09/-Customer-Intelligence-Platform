"""
Retention recommendations — campaign prioritization and target lists.
"""

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header, format_currency
from dashboard.components.cards import render_kpi_card
from dashboard.components.filters import render_sidebar_filters
from dashboard.components.tables import render_interactive_table
from dashboard.components.charts import plot_recommendation_chart
from dashboard.utils.cache import load_global_intelligence_data

inject_styles()


def render_recommendations_page():
    render_page_header(
        title="Retention Recommendations",
        subtitle="Review prioritized retention actions, campaign volumes, and expected value impact across the portfolio.",
        eyebrow="Retention",
    )

    df_intel = load_global_intelligence_data()
    if df_intel.empty:
        st.error("Analytics data is not loaded.")
        return

    df_filtered = render_sidebar_filters(df_intel)

    total_savings = df_filtered["estimated_revenue_saved"].sum() if not df_filtered.empty else 0.0
    crit_count = len(df_filtered[df_filtered["recommendation_priority"] == "Critical"])
    high_count = len(df_filtered[df_filtered["recommendation_priority"] == "High"])
    med_count = len(df_filtered[df_filtered["recommendation_priority"] == "Medium"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(format_currency(total_savings), "Total Retention Value", accent="success")
    with c2:
        render_kpi_card(f"{crit_count:,}", "Critical Actions", accent="danger")
    with c3:
        render_kpi_card(f"{high_count:,}", "High Priority", accent="warning")
    with c4:
        render_kpi_card(f"{med_count:,}", "Medium Priority", accent="primary")

    st.divider()

    render_section_header("Campaign Volume by Priority")
    st.plotly_chart(plot_recommendation_chart(df_filtered), use_container_width=True)

    st.divider()

    render_section_header("Campaign Targets")

    unique_campaigns = ["All"] + sorted(list(df_filtered["primary_recommendation"].dropna().unique()))
    selected_camp = st.selectbox("Filter by campaign type", unique_campaigns)

    df_watchlist = df_filtered.copy()
    if selected_camp != "All":
        df_watchlist = df_watchlist[df_watchlist["primary_recommendation"] == selected_camp]

    display_cols = [
        "customer_id", "primary_recommendation", "recommendation_priority",
        "churn_probability", "predicted_ltv", "estimated_revenue_saved",
    ]
    render_interactive_table(
        df_watchlist[display_cols].sort_values(by="estimated_revenue_saved", ascending=False),
        page_size=15,
        key="camp_table",
    )


if __name__ == "__main__":
    render_recommendations_page()
