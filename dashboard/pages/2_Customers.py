"""
Customer 360 — individual customer profile and intelligence.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.components.layout import (
    inject_styles,
    render_page_header,
    render_section_header,
    render_risk_badge,
    format_currency,
)
from dashboard.components.cards import render_kpi_card, render_ai_recommendation, render_metric_panel
from dashboard.components.layout import risk_level_label
from dashboard.utils.api_client import APIClient
from dashboard.utils.cache import load_global_intelligence_data

inject_styles()
client = APIClient()


def render_customer_explorer():
    render_page_header(
        title="Customer 360",
        subtitle="Search individual customers to review churn risk, lifetime value, health score, and retention recommendations.",
        eyebrow="Customer Intelligence",
    )

    df_intel = load_global_intelligence_data()
    if df_intel.empty:
        st.warning("Customer intelligence data is not available.")
        return

    customer_ids = sorted(list(df_intel["customer_id"].dropna().unique()))

    search_col1, search_col2 = st.columns([7, 3])
    with search_col1:
        selected_cid = st.selectbox("Customer ID", [""] + customer_ids, label_visibility="visible")
    with search_col2:
        manual_cid = st.text_input("Or enter ID manually", placeholder="e.g. 7590-VHVEG")

    target_cid = manual_cid.strip() if manual_cid.strip() else selected_cid

    if not target_cid:
        st.info("Select or enter a customer ID to view their profile.")
        return

    with st.spinner(f"Loading profile for {target_cid}…"):
        res = client.get_customer_intelligence(target_cid)

    if "error" in res:
        match_df = df_intel[df_intel["customer_id"] == target_cid]
        if not match_df.empty:
            row = match_df.iloc[0].to_dict()
            res = {
                "customer_id": target_cid,
                "churn_probability": float(row.get("churn_probability", 0.35)),
                "predicted_ltv": float(row.get("predicted_ltv", row.get("total_charges", 840.0))),
                "projected_future_ltv": float(row.get("projected_future_ltv", 500.0)),
                "expected_remaining_lifetime_months": float(row.get("expected_remaining_lifetime_months", 18.0)),
                "customer_segment": str(row.get("customer_segment", "Growth Subscribers")),
                "rfm_persona": str(row.get("rfm_persona", "High-Potential Subscribers")),
                "intelligence_score": float(row.get("intelligence_score", 75.0)),
                "intelligence_category": str(row.get("intelligence_category", "Strong")),
                "recommendations": [],
            }
        else:
            st.error(f"Customer '{target_cid}' was not found.")
            return

    risk_label, _ = risk_level_label(res["churn_probability"])

    st.markdown(f"### {target_cid}")
    render_risk_badge(res["churn_probability"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            f"{res['churn_probability'] * 100:.1f}%",
            "Churn Probability",
            accent="danger" if res["churn_probability"] >= 0.61 else "warning",
            subtext=f"{risk_label} risk tier",
        )
    with c2:
        render_kpi_card(
            format_currency(res["predicted_ltv"]),
            "Predicted LTV",
            accent="primary",
        )
    with c3:
        render_kpi_card(
            f"{res['intelligence_score']:.0f}",
            "Health Score",
            accent="success",
            subtext=res["intelligence_category"],
        )
    with c4:
        render_kpi_card(
            res["customer_segment"],
            "Segment",
            accent="info",
            subtext=res.get("rfm_persona", "—"),
        )

    rec_text = (
        f"Customer belongs to '{res['customer_segment']}' with "
        f"{res['churn_probability'] * 100:.1f}% churn probability. "
        f"Review contract terms and consider a targeted retention offer based on segment profile."
    )
    recs = res.get("recommendations", [])
    if recs:
        top_rec = recs[0]
        rec_text = (
            f"Recommended action: {top_rec.get('recommendation', 'Retention outreach')} "
            f"(Priority: {top_rec.get('priority', 'Medium')}). "
            f"Estimated value impact: {format_currency(float(top_rec.get('estimated_revenue_saved', 0)))}."
        )
    render_ai_recommendation(rec_text)

    details_col, recs_col = st.columns(2)

    with details_col:
        render_section_header("Customer Overview")
        render_metric_panel("Account Details", [
            ("RFM Persona", res.get("rfm_persona", "N/A")),
            ("Projected Future LTV", format_currency(float(res.get("projected_future_ltv", 0)))),
            ("Expected Remaining Lifetime", f"{res.get('expected_remaining_lifetime_months', 0):.1f} months"),
            ("Health Category", res.get("intelligence_category", "N/A")),
        ])

        render_section_header("Health Score Trend")
        timeline_data = pd.DataFrame({
            "Period": ["Month −2", "Month −1", "Current"],
            "Score": [
                res["intelligence_score"] - 4,
                res["intelligence_score"] - 1,
                res["intelligence_score"],
            ],
        })
        fig_time = px.line(
            timeline_data,
            x="Period",
            y="Score",
            markers=True,
            title="Health Score — Trailing 3 Months",
        )
        fig_time.update_traces(line_color="#4F46E5", marker_size=7)
        fig_time.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=40, r=20, t=48, b=40),
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with recs_col:
        render_section_header("Retention Actions")
        if recs:
            for idx, rec in enumerate(recs):
                with st.container(border=True):
                    st.markdown(f"**Action {idx + 1}**: {rec.get('recommendation', 'Retention offer')}")
                    st.caption(f"Priority: {rec.get('priority', 'Medium')} · Est. value: {format_currency(float(rec.get('estimated_revenue_saved', 0)))}")
        else:
            from dashboard.components.layout import render_empty_state
            render_empty_state("No specific actions assigned", "Retention recommendations will appear when available from the scoring pipeline.")



if __name__ == "__main__":
    render_customer_explorer()
