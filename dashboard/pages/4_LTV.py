"""
LTV analytics — lifetime value forecasting and portfolio analysis.
"""

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header, format_currency
from dashboard.components.cards import render_kpi_card
from dashboard.components.filters import render_sidebar_filters
from dashboard.components.charts import plot_ltv_distribution, plot_top_revenue_bar
from dashboard.utils.cache import load_global_intelligence_data

inject_styles()


def render_ltv_page():
    render_page_header(
        title="LTV Intelligence",
        subtitle="Forecast customer lifetime value, review billing distributions, and assess revenue concentration.",
        eyebrow="Customer Intelligence",
    )

    df_intel = load_global_intelligence_data()
    if df_intel.empty:
        st.error("Analytics data is not loaded.")
        return

    df_filtered = render_sidebar_filters(df_intel)

    total_projected = df_filtered["projected_future_ltv"].sum() if not df_filtered.empty else 0.0
    avg_projected = df_filtered["projected_future_ltv"].mean() if not df_filtered.empty else 0.0
    avg_hist = df_filtered["predicted_ltv"].mean() if not df_filtered.empty else 0.0
    hist_sum = df_filtered["predicted_ltv"].sum() if not df_filtered.empty else 1.0
    ratio = total_projected / (hist_sum + 1e-6) if not df_filtered.empty else 0.0

    render_section_header("LTV Portfolio Metrics")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        render_kpi_card(format_currency(total_projected), "Total Projected LTV", accent="primary")
    with f_col2:
        render_kpi_card(format_currency(avg_projected), "Avg Projected LTV", accent="info", subtext="Forward-looking")
    with f_col3:
        render_kpi_card(format_currency(avg_hist), "Avg Historical LTV", accent="default", subtext="Realized spend")
    with f_col4:
        render_kpi_card(f"{ratio:.2f}×", "LTV Expansion Multiple", accent="success")

    st.divider()

    render_section_header("Distribution & Concentration")
    col_dist, col_top = st.columns(2)
    with col_dist:
        st.plotly_chart(plot_ltv_distribution(df_filtered), use_container_width=True)
    with col_top:
        st.plotly_chart(plot_top_revenue_bar(df_filtered), use_container_width=True)


if __name__ == "__main__":
    render_ltv_page()
