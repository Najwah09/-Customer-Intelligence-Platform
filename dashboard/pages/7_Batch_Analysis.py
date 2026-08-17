"""
Batch analysis — bulk customer scoring via CSV upload.
"""

import streamlit as st
import pandas as pd

from dashboard.components.layout import inject_styles, render_page_header, render_section_header
from dashboard.utils.api_client import APIClient
from dashboard.utils.export import convert_df_to_csv, convert_df_to_excel

inject_styles()
client = APIClient()


def render_batch_page():
    render_page_header(
        title="Batch Analysis",
        subtitle="Upload customer ID lists to score churn risk, calculate LTV forecasts, and export results in bulk.",
        eyebrow="System",
    )

    render_section_header("Upload Customer IDs")

    sample_csv = (
        "customer_id\n"
        "7590-VHVEG\n"
        "5575-GNVDE\n"
        "3668-QPYBK\n"
        "7795-CFOCW\n"
        "9237-HQJOC\n"
    )
    st.download_button(
        label="Download sample CSV template",
        data=sample_csv,
        file_name="sample_customer_ids.csv",
        mime="text/csv",
    )

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if not uploaded_file:
        st.info("Upload a CSV file with a `customer_id` column to begin batch scoring.")
        return

    try:
        df_uploaded = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        return

    st.dataframe(df_uploaded.head(5), use_container_width=True, hide_index=True)

    id_col = None
    for col in df_uploaded.columns:
        if str(col).strip().lower() in ["customer_id", "customerid", "id", "account_id"]:
            id_col = col
            break

    if not id_col:
        st.error("No valid customer ID column found. Expected header: `customer_id`.")
        return

    customer_ids = [str(x).strip() for x in df_uploaded[id_col].dropna().unique()]
    st.caption(f"{len(customer_ids)} unique customer IDs identified.")

    if st.button("Run batch scoring", type="primary"):
        with st.spinner("Processing batch scoring…"):
            res_list = client.batch_score_customers(customer_ids)

        if not res_list or "error" in res_list[0]:
            st.error(res_list[0].get("error", "Batch scoring failed."))
            return

        df_results = pd.DataFrame(res_list)
        st.success(f"Scored {len(df_results)} customers successfully.")

        render_section_header("Results Preview")
        st.dataframe(df_results.head(10), use_container_width=True, hide_index=True)

        render_section_header("Export")
        col_csv, col_xlsx = st.columns(2)
        with col_csv:
            st.download_button(
                label="Download CSV",
                data=convert_df_to_csv(df_results),
                file_name="batch_scored_intelligence.csv",
                mime="text/csv",
            )
        with col_xlsx:
            st.download_button(
                label="Download Excel",
                data=convert_df_to_excel(df_results),
                file_name="batch_scored_intelligence.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )


if __name__ == "__main__":
    render_batch_page()
