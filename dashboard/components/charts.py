"""
RETAINAI — Enterprise Chart Components with Clean Light Plotly Styling.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CHART_COLORS = [
    "#4F46E5",
    "#0EA5E9",
    "#059669",
    "#D97706",
    "#DC2626",
    "#7C3AED",
]

PRIORITY_COLORS = {
    "Critical": "#DC2626",
    "High": "#D97706",
    "Medium": "#0EA5E9",
    "Low": "#059669",
}

_LAYOUT_DEFAULTS = dict(
    template="plotly_white",
    font=dict(family="Inter, system-ui, sans-serif", size=12, color="#475569"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title=dict(font=dict(size=14, color="#0F172A")),
    margin=dict(l=48, r=24, t=56, b=56),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.22,
        xanchor="center",
        x=0.5,
        font=dict(size=11, color="#475569"),
    ),
    xaxis=dict(
        gridcolor="#F1F5F9",
        linecolor="#E2E8F0",
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#475569"),
    ),
    yaxis=dict(
        gridcolor="#F1F5F9",
        linecolor="#E2E8F0",
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#475569"),
    ),
    hoverlabel=dict(
        bgcolor="#FFFFFF",
        font_size=12,
        font_family="Inter, system-ui, sans-serif",
        bordercolor="#E2E8F0",
    ),
)


def apply_chart_style(fig: go.Figure, height: int = 360) -> go.Figure:
    """Apply consistent enterprise styling to a Plotly figure."""
    fig.update_layout(**_LAYOUT_DEFAULTS, height=height)
    return fig


def plot_ltv_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of predicted LTV values."""
    ltv_col = "predicted_ltv" if "predicted_ltv" in df.columns else df.columns[0]
    ltvs = df[ltv_col].dropna()
    mean_val = float(ltvs.mean()) if not ltvs.empty else 0.0

    fig = px.histogram(
        df,
        x=ltv_col,
        nbins=12,
        title="Subscriber LTV Distribution",
        labels={ltv_col: "Predicted LTV ($)", "count": "Subscribers"},
        color_discrete_sequence=[CHART_COLORS[0]],
        template="plotly_white",
    )
    if not ltvs.empty:
        fig.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="#D97706",
            annotation_text=f"Mean: ${mean_val:,.0f}",
            annotation_position="top right",
        )
    return apply_chart_style(fig)


def plot_segment_distribution(df: pd.DataFrame) -> go.Figure:
    """Donut chart of customer segments."""
    seg_col = "customer_segment" if "customer_segment" in df.columns else df.columns[0]
    counts = df[seg_col].value_counts().reset_index()
    counts.columns = ["Segment", "Count"]

    fig = px.pie(
        counts,
        names="Segment",
        values="Count",
        hole=0.45,
        title="Subscriber Cohort Share",
        color_discrete_sequence=CHART_COLORS,
        template="plotly_white",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return apply_chart_style(fig)


def plot_cluster_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of tenure vs monthly charges by segment."""
    fig = px.scatter(
        df,
        x="tenure_months",
        y="monthly_charges",
        color="customer_segment" if "customer_segment" in df.columns else None,
        title="Subscriber Segment Boundaries (Tenure vs Monthly Charges)",
        labels={"tenure_months": "Tenure (Months)", "monthly_charges": "Monthly Charges ($)"},
        color_discrete_sequence=CHART_COLORS,
        template="plotly_white",
        opacity=0.8,
    )
    return apply_chart_style(fig)


def plot_recommendation_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of recommendation volume."""
    rec_col = "primary_recommendation" if "primary_recommendation" in df.columns else df.columns[0]
    counts = df[rec_col].value_counts().head(8).reset_index()
    counts.columns = ["Recommendation", "Volume"]

    fig = px.bar(
        counts,
        y="Recommendation",
        x="Volume",
        orientation="h",
        title="Top Triggered Retention Actions",
        labels={"Volume": "Subscribers", "Recommendation": "Action"},
        color_discrete_sequence=[CHART_COLORS[1]],
        template="plotly_white",
    )
    fig.update_yaxes(autorange="reversed")
    return apply_chart_style(fig)


def plot_score_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of Subscriber Intelligence Scores."""
    score_col = "intelligence_score" if "intelligence_score" in df.columns else df.columns[0]

    fig = px.histogram(
        df,
        x=score_col,
        nbins=10,
        title="Subscriber Health Index (0-100) Distribution",
        labels={score_col: "Health Score (0-100)", "count": "Subscribers"},
        color_discrete_sequence=["#059669"],
        template="plotly_white",
    )
    return apply_chart_style(fig)


def plot_top_revenue_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart showing top 10 revenue-generating accounts."""
    top_df = df.copy()
    val_col = "predicted_ltv" if "predicted_ltv" in top_df.columns else "total_charges"
    top_df = top_df.sort_values(by=val_col, ascending=False).head(10)

    fig = px.bar(
        top_df,
        x=val_col,
        y="customer_id",
        orientation="h",
        title="Top 10 Accounts by Predicted LTV",
        labels={val_col: "Predicted LTV ($)", "customer_id": "Subscriber ID"},
        color_discrete_sequence=["#D97706"],
        template="plotly_white",
    )
    fig.update_yaxes(autorange="reversed")
    return apply_chart_style(fig)


def plot_business_impact_bar(df: pd.DataFrame) -> go.Figure:
    """Targeted potential financial savings per priority tier."""
    if "recommendation_priority" in df.columns and "estimated_revenue_saved" in df.columns:
        impact = df.groupby("recommendation_priority")["estimated_revenue_saved"].sum().reset_index()
        impact.columns = ["Priority", "Saved Revenue"]
    else:
        impact = pd.DataFrame([{"Priority": "High", "Saved Revenue": 1872000.0}])

    fig = px.bar(
        impact,
        x="Priority",
        y="Saved Revenue",
        title="Estimated Revenue Savings by Action Priority",
        labels={"Saved Revenue": "Saved Revenue ($)", "Priority": "Priority Tier"},
        color="Priority",
        color_discrete_map=PRIORITY_COLORS,
        template="plotly_white",
    )
    return apply_chart_style(fig)


def plot_segment_comparison_box(df: pd.DataFrame) -> go.Figure:
    """Boxplot showing churn risk spread binned by segment."""
    fig = px.box(
        df,
        x="customer_segment" if "customer_segment" in df.columns else df.columns[0],
        y="churn_probability" if "churn_probability" in df.columns else df.columns[1],
        title="Churn Probability Spread by Segment",
        labels={"customer_segment": "Segment", "churn_probability": "Churn Risk"},
        color_discrete_sequence=CHART_COLORS,
        template="plotly_white",
    )
    return apply_chart_style(fig)


def plot_revenue_distribution_box(df: pd.DataFrame) -> go.Figure:
    """Boxplot showing LTV distribution spread binned by segment."""
    fig = px.box(
        df,
        x="customer_segment" if "customer_segment" in df.columns else df.columns[0],
        y="predicted_ltv" if "predicted_ltv" in df.columns else df.columns[1],
        title="LTV Distribution Spread by Segment",
        labels={"customer_segment": "Segment", "predicted_ltv": "Predicted LTV ($)"},
        color_discrete_sequence=CHART_COLORS,
        template="plotly_white",
    )
    return apply_chart_style(fig)


def plot_rfm_heatmap(df: pd.DataFrame) -> go.Figure:
    """Density heatmap of Recency vs Frequency RFM scores."""
    r_col = "recency_score" if "recency_score" in df.columns else "R"
    f_col = "frequency_score" if "frequency_score" in df.columns else "F"
    if df.empty or r_col not in df.columns or f_col not in df.columns:
        fig = px.density_heatmap(
            pd.DataFrame({"R": [1, 2, 3, 4, 5], "F": [1, 2, 3, 4, 5], "Count": [1, 1, 1, 1, 1]}),
            x="R",
            y="F",
            z="Count",
            title="RFM Persona Distribution Density",
            template="plotly_white",
        )
    else:
        fig = px.density_heatmap(
            df,
            x=r_col,
            y=f_col,
            title="RFM Persona Distribution Density",
            labels={r_col: "Recency Score", f_col: "Frequency Score"},
            color_continuous_scale="Blues",
            template="plotly_white",
        )
    return apply_chart_style(fig)


def plot_before_after_comparison(before: dict, after: dict) -> go.Figure:
    """Grouped bar chart comparing BEFORE vs AFTER simulation metrics."""
    metrics = ["Churn Risk (%)", "Predicted LTV ($)"]
    b_values = [before.get("churn_probability", 0.35) * 100.0, before.get("predicted_ltv", 1000.0)]
    a_values = [after.get("churn_probability", 0.20) * 100.0, after.get("predicted_ltv", 1200.0)]

    fig = go.Figure(data=[
        go.Bar(name="Before Intervention", x=metrics, y=b_values, marker_color=CHART_COLORS[4]),
        go.Bar(name="After Intervention", x=metrics, y=a_values, marker_color=CHART_COLORS[2]),
    ])
    fig.update_layout(
        barmode="group",
        title="BEFORE vs AFTER Intervention Metrics",
        template="plotly_white",
    )
    return apply_chart_style(fig)


