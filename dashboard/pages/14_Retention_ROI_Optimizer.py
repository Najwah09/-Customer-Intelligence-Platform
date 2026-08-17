"""
Retention ROI Optimizer — strategy comparison and ranking.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header, format_currency
from dashboard.components.cards import render_strategy_recommendation
from dashboard.components.charts import apply_chart_style, CHART_COLORS
from dashboard.utils.cache import load_global_intelligence_data
from backend.services.ai_tools import ai_tools

inject_styles()


def render_retention_roi_optimizer_page():
    render_page_header(
        title="ROI Optimizer",
        subtitle="Compare retention strategies by intervention cost, expected retention, net value, and estimated ROI.",
        eyebrow="Retention",
    )

    df_intel = load_global_intelligence_data()
    customer_ids = (
        sorted(list(df_intel["customer_id"].dropna().unique()))
        if not df_intel.empty
        else ["0003-MKNFE"]
    )

    render_section_header("Select Customer")
    target_cid = st.selectbox("Customer ID", customer_ids, label_visibility="collapsed")

    roi_res = ai_tools.calculate_retention_roi(target_cid)
    if "error" in roi_res:
        st.error(roi_res["error"])
        return

    st.divider()

    render_strategy_recommendation(roi_res["recommendation_reasoning"])

    ranked_strats = roi_res["ranked_strategies"]
    df_strats = pd.DataFrame(ranked_strats)

    render_section_header("Strategy Comparison")

    display_df = df_strats[[
        "strategy", "intervention_cost", "retention_probability",
        "expected_retained_value", "expected_net_value", "estimated_roi_percent", "assumptions",
    ]].copy()
    display_df.columns = [
        "Strategy", "Cost", "Retention Prob.",
        "Retained Value", "Net Value", "ROI (%)", "Assumptions",
    ]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()

    render_section_header("Net Value by Strategy")
    fig = px.bar(
        df_strats,
        x="strategy",
        y="expected_net_value",
        title=f"Expected Net Value — {target_cid}",
        labels={"expected_net_value": "Net Value ($)", "strategy": "Strategy"},
        color_discrete_sequence=[CHART_COLORS[0]],
    )
    fig.update_layout(showlegend=False)

    best_idx = df_strats["expected_net_value"].idxmax()
    fig.update_traces(
        marker_color=[
            CHART_COLORS[2] if i == best_idx else CHART_COLORS[4]
            for i in range(len(df_strats))
        ]
    )

    st.plotly_chart(apply_chart_style(fig), use_container_width=True)


if __name__ == "__main__":
    render_retention_roi_optimizer_page()
