"""
Segment analytics — cluster distribution and comparative analysis.
"""

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header
from dashboard.components.cards import render_kpi_card
from dashboard.components.filters import render_sidebar_filters
from dashboard.components.charts import (
    plot_segment_distribution,
    plot_cluster_scatter,
    plot_revenue_distribution_box,
    plot_segment_comparison_box,
)
from dashboard.utils.cache import load_global_intelligence_data

inject_styles()


def render_segments_page():
    render_page_header(
        title="Segment Intelligence",
        subtitle="Analyze customer cohort distributions, cluster boundaries, and risk comparison across segments.",
        eyebrow="Customer Intelligence",
    )

    df_intel = load_global_intelligence_data()
    if df_intel.empty:
        st.error("Analytics data is not loaded.")
        return

    df_filtered = render_sidebar_filters(df_intel)

    segments = df_filtered["customer_segment"].unique()
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_kpi_card(str(len(segments)), "Active Segments", accent="primary", subtext="K-Means clusters")
    with s2:
        high_val = df_filtered[df_filtered["customer_segment"].str.contains("High-Value", case=False, na=False)]
        render_kpi_card(f"{len(high_val):,}", "High-Value", accent="success", subtext="Core revenue segment")
    with s3:
        loyal = df_filtered[df_filtered["customer_segment"].str.contains("Loyal", case=False, na=False)]
        render_kpi_card(f"{len(loyal):,}", "Loyal", accent="info", subtext="Low attrition profile")
    with s4:
        budget = df_filtered[df_filtered["customer_segment"].str.contains("Budget", case=False, na=False)]
        render_kpi_card(f"{len(budget):,}", "Budget", accent="warning", subtext="Price-sensitive segment")

    st.divider()

    render_section_header("Distribution & Clusters")
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(plot_segment_distribution(df_filtered), use_container_width=True)
    with col_right:
        st.plotly_chart(plot_cluster_scatter(df_filtered), use_container_width=True)

    st.divider()

    render_section_header("Comparative Analysis")
    col_spend, col_churn = st.columns(2)
    with col_spend:
        st.plotly_chart(plot_revenue_distribution_box(df_filtered), use_container_width=True)
    with col_churn:
        st.plotly_chart(plot_segment_comparison_box(df_filtered), use_container_width=True)


if __name__ == "__main__":
    render_segments_page()
