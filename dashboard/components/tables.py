"""
Data table components with search, pagination, and formatting.
"""

import streamlit as st
import pandas as pd


def _format_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert snake_case column names to readable labels."""
    renamed = {}
    for col in df.columns:
        label = col.replace("_", " ").title()
        label = label.replace("Ltv", "LTV").replace("Id", "ID").replace("Rfm", "RFM")
        renamed[col] = label
    return df.rename(columns=renamed)


def render_interactive_table(
    df: pd.DataFrame,
    page_size: int = 15,
    key: str = "table",
    search: bool = True,
):
    """Render a searchable, paginated dataframe."""
    if df.empty:
        from dashboard.components.layout import render_empty_state
        render_empty_state("No records found", "Adjust your filters or search criteria to view matching customers.")
        return


    display_df = _format_column_names(df.copy())

    if search:
        search_term = st.text_input(
            "Search",
            placeholder="Filter by customer ID or value…",
            key=f"{key}_search",
            label_visibility="collapsed",
        )
        if search_term:
            mask = display_df.astype(str).apply(
                lambda row: row.str.contains(search_term, case=False, na=False).any(),
                axis=1,
            )
            display_df = display_df[mask]

    total_rows = len(display_df)
    total_pages = max(1, (total_rows - 1) // page_size + 1)

    nav_col1, nav_col2, nav_col3 = st.columns([2, 1, 2])
    with nav_col2:
        current_page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
            key=f"{key}_page",
            label_visibility="collapsed",
        )

    start_idx = (current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_rows)
    df_subset = display_df.iloc[start_idx:end_idx]

    st.dataframe(
        df_subset,
        use_container_width=True,
        hide_index=True,
        height=min(52 + len(df_subset) * 35, 520),
    )
    st.markdown(
        f'<p class="table-caption">Showing {start_idx + 1}–{end_idx} of {total_rows:,} records</p>',
        unsafe_allow_html=True,
    )
