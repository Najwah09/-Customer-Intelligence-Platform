"""
What-If Simulator — model-driven intervention scenario analysis.
"""

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header, format_currency
from dashboard.components.cards import render_kpi_card
from dashboard.components.charts import apply_chart_style, CHART_COLORS, plot_before_after_comparison
from dashboard.utils.cache import load_global_intelligence_data
from backend.services.ai_tools import ai_tools, _safe_int, _safe_float

inject_styles()


def render_what_if_simulator_page():
    render_page_header(
        title="What-If Simulator",
        subtitle="Modify customer parameters and compare predicted churn risk and LTV before and after a retention intervention.",
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

    cust = ai_tools.get_customer(target_cid)
    if "error" in cust:
        st.error(cust["error"])
        return

    st.divider()

    render_section_header("Scenario Configuration")

    col_orig, col_mod = st.columns(2)

    monthly_val = _safe_float(cust.get("monthly_charges"), 70.0)
    tenure_val = _safe_int(cust.get("tenure_months"), 12)
    churn_val = _safe_float(cust.get("churn_probability"), 0.35)

    with col_orig:
        with st.container(border=True):
            st.markdown("### Current Scenario")
            st.markdown(f"• **Contract**: `{cust.get('contract_type', 'Month-to-month')}`")
            st.markdown(f"• **Monthly Charges**: `${monthly_val:,.2f}`")
            st.markdown(f"• **Tech Support**: `{cust.get('tech_support', 'No')}`")
            st.markdown(f"• **Tenure**: `{tenure_val} months`")
            st.markdown(f"• **Churn Risk**: `{churn_val * 100:.1f}%`")

    with col_mod:
        with st.container(border=True):
            st.markdown("### Simulated Scenario")

            contract_options = ["Month-to-month", "One year", "Two year"]
            current_contract = cust.get("contract_type", "Month-to-month")
            new_contract = st.selectbox(
                "Contract Type",
                contract_options,
                index=contract_options.index(current_contract) if current_contract in contract_options else 0,
            )
            discount_pct = st.slider("Billing Discount (%)", 0, 30, 10, step=5)
            new_charges = float(cust.get("monthly_charges", 70.0)) * (1.0 - (discount_pct / 100.0))
            st.caption(f"Adjusted monthly charge: ${new_charges:.2f}")
            new_tech_support = st.radio("Tech Support", ["Yes", "No"], index=0 if cust.get("tech_support") == "Yes" else 1)

    st.divider()

    if st.button("Run simulation", type="primary"):
        modified_params = {
            "contract_type": new_contract,
            "monthly_charges": new_charges,
            "tech_support": new_tech_support,
        }
        sim_res = ai_tools.simulate_intervention(target_cid, modified_params)

        b = sim_res["before"]
        a = sim_res["after"]

        render_section_header("Predicted Outcomes")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_kpi_card(
                f"{b['churn_probability'] * 100:.1f}% → {a['churn_probability'] * 100:.1f}%",
                "Churn Risk",
                accent="success" if a['churn_probability'] < b['churn_probability'] else "danger",
                subtext=f"Delta: {(a['churn_probability'] - b['churn_probability']) * 100:.1f}%",
            )
        with c2:
            render_kpi_card(
                f"{format_currency(b['predicted_ltv'])} → {format_currency(a['predicted_ltv'])}",
                "Predicted LTV",
                accent="primary",
                subtext=f"Change: {format_currency(a['predicted_ltv'] - b['predicted_ltv'])}",
            )
        with c3:
            render_kpi_card(
                format_currency(sim_res["difference"]["potential_value_saved"]),
                "Potential Value Saved",
                accent="success",
                subtext="Probability-weighted value retained",
            )
        with c4:
            render_kpi_card(
                f"{sim_res['difference']['churn_reduction_percent']:.1f}%",
                "Relative Churn Reduction",
                accent="success",
                subtext="Percentage decrease in risk",
            )

        st.divider()

        st.plotly_chart(plot_before_after_comparison(b, a), use_container_width=True)

        if "disclaimer" in sim_res:
            st.caption(f"Note: {sim_res['disclaimer']}")


if __name__ == "__main__":
    render_what_if_simulator_page()
