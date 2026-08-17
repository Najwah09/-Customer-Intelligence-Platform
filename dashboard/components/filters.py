"""
Sidebar filters and cohort controls.
"""

import pandas as pd
import streamlit as st

from dashboard.components.layout import render_sidebar_branding


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return filtered dataframe."""
    render_sidebar_branding()

    st.sidebar.subheader("Filters")

    segments = ["All"] + sorted(list(df["customer_segment"].dropna().unique()))
    selected_segment = st.sidebar.selectbox("Segment", segments, key="filter_seg")

    risk_options = ["All", "High (≥ 61%)", "Medium (40–61%)", "Low (< 40%)"]
    selected_risk = st.sidebar.selectbox("Churn Risk", risk_options, key="filter_risk")

    score_cats = ["All"] + sorted(list(df["intelligence_category"].dropna().unique()))
    selected_score_cat = st.sidebar.selectbox("Health Category", score_cats, key="filter_score")

    personas = ["All"] + sorted(list(df["rfm_persona"].dropna().unique()))
    selected_persona = st.sidebar.selectbox("RFM Persona", personas, key="filter_rfm")

    df_filtered = df.copy()

    if selected_segment != "All":
        df_filtered = df_filtered[df_filtered["customer_segment"] == selected_segment]

    if selected_risk == "High (≥ 61%)":
        df_filtered = df_filtered[df_filtered["churn_probability"] >= 0.61]
    elif selected_risk == "Medium (40–61%)":
        df_filtered = df_filtered[
            (df_filtered["churn_probability"] >= 0.40)
            & (df_filtered["churn_probability"] < 0.61)
        ]
    elif selected_risk == "Low (< 40%)":
        df_filtered = df_filtered[df_filtered["churn_probability"] < 0.40]

    if selected_score_cat != "All":
        df_filtered = df_filtered[df_filtered["intelligence_category"] == selected_score_cat]

    if selected_persona != "All":
        df_filtered = df_filtered[df_filtered["rfm_persona"] == selected_persona]

    active_filters = sum([
        selected_segment != "All",
        selected_risk != "All",
        selected_score_cat != "All",
        selected_persona != "All",
    ])

    if active_filters > 0:
        if st.sidebar.button("Reset filters", use_container_width=True):
            for key in ("filter_seg", "filter_risk", "filter_score", "filter_rfm"):
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.sidebar.caption(f"Showing **{len(df_filtered):,}** of **{len(df):,}** customers")


    return df_filtered
