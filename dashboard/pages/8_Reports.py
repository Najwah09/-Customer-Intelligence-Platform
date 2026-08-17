"""
Executive reports — view and download generated intelligence reports.
"""

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header
from dashboard.utils.cache import load_report_markdown

inject_styles()


def render_reports_page():
    render_page_header(
        title="Executive Reports",
        subtitle="View and download executive summaries, business impact analyses, and model evaluation reports.",
        eyebrow="Reporting",
    )

    reports_map = {
        "Executive Summary": "executive_summary.md",
        "Business Impact & ROI": "business_impact.md",
        "LTV Modeling Performance": "ltv_summary.md",
        "Segment Profiles": "segment_profiles.md",
        "Campaign Recommendations": "recommendation_summary.md",
        "Scoring Methodology": "customer_intelligence.md",
    }

    selected_title = st.selectbox("Select report", list(reports_map.keys()))
    report_content = load_report_markdown(reports_map[selected_title])

    st.divider()

    with st.container(border=True):
        st.markdown(report_content)

    st.divider()

    st.download_button(
        label=f"Download {selected_title}",
        data=report_content,
        file_name=reports_map[selected_title],
        mime="text/markdown",
    )


if __name__ == "__main__":
    render_reports_page()
