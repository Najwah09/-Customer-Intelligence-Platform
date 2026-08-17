"""
System operations — health monitoring, model registry, and drift tracking.
"""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header
from dashboard.components.cards import render_kpi_card
from dashboard.components.charts import apply_chart_style, CHART_COLORS
from dashboard.utils.api_client import APIClient

inject_styles()

BASE_DIR = Path(__file__).resolve().parents[2]


def _patch_client(c: APIClient) -> APIClient:
    import httpx

    def _safe_get(path: str):
        try:
            url = f"{c.base_url}{path}"
            resp = httpx.get(url, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
            return {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    c._safe_get = _safe_get
    return c


client = _patch_client(APIClient())


def _safe_api_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}


def render_operations_page() -> None:
    render_page_header(
        title="System Health",
        subtitle="Monitor API status, model registry, data drift, ingestion pipeline, and scheduled jobs.",
        eyebrow="System",
    )

    render_section_header("Service Status")
    health_col, ready_col, metrics_col = st.columns(3)

    with health_col:
        health = _safe_api_call(lambda: client._safe_get("/health"))
        status = health.get("status", "unknown") if isinstance(health, dict) else "error"
        render_kpi_card(
            status.upper(),
            "API Status",
            accent="success" if status == "healthy" else "danger",
        )

    with ready_col:
        ready = _safe_api_call(lambda: client._safe_get("/ready"))
        r_status = ready.get("status", "unknown") if isinstance(ready, dict) else "error"
        render_kpi_card(r_status.upper(), "Readiness", accent="primary")

    with metrics_col:
        snap = _safe_api_call(lambda: client._safe_get("/metrics"))
        total_req = snap.get("requests", {}).get("total", "N/A") if isinstance(snap, dict) else "N/A"
        render_kpi_card(str(total_req), "Total Requests", accent="default")

    st.divider()

    render_section_header("Ingestion Pipeline")
    sync_state = _safe_api_call(lambda: client._safe_get("/ingest/state"))
    if not isinstance(sync_state, dict) or "error" in sync_state:
        state_file = BASE_DIR / "data" / "sync_state.json"
        if state_file.exists():
            with open(state_file, "r") as f:
                sync_state = json.load(f)
        else:
            sync_state = {}

    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        last_sync = sync_state.get("last_auto_sync", "Never")
        last_sync_str = last_sync[:19].replace("T", " ") if isinstance(last_sync, str) and "T" in last_sync else str(last_sync)
        render_kpi_card(last_sync_str if last_sync else "—", "Last Sync", accent="primary")
    with s_col2:
        render_kpi_card(f"{sync_state.get('records_processed_today', 0):,}", "Records Today", accent="success")
    with s_col3:
        last_pred = sync_state.get("last_prediction_time", "—")
        last_pred_str = last_pred[:19].replace("T", " ") if isinstance(last_pred, str) and "T" in last_pred else str(last_pred)
        render_kpi_card(last_pred_str if last_pred else "—", "Last Prediction", accent="info")
    with s_col4:
        last_drift = sync_state.get("last_drift_check", "—")
        last_drift_str = last_drift[:10] if isinstance(last_drift, str) and len(last_drift) >= 10 else str(last_drift)
        render_kpi_card(last_drift_str if last_drift else "—", "Last Drift Check", accent="warning")

    st.divider()

    render_section_header("Model Registry")
    registry = _safe_api_call(lambda: client._safe_get("/observability/registry"))
    if isinstance(registry, dict) and "error" not in registry:
        rows = []
        for model_name, versions in registry.items():
            for v in versions:
                rows.append({
                    "Model": model_name,
                    "Version": v.get("version"),
                    "Status": v.get("status"),
                    "Type": v.get("model_type"),
                    "Tags": ", ".join(v.get("tags", [])),
                    "Registered": v.get("registered_at", "")[:10],
                })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No models registered. Run `python scripts/seed_registry.py`.")
    else:
        st.warning("Registry unavailable — ensure the FastAPI backend is running.")

    st.divider()

    render_section_header("Drift Monitoring")
    drift_dir = BASE_DIR / "reports" / "drift"
    if drift_dir.exists():
        history_files = sorted(drift_dir.glob("*.json"), reverse=True)
        if history_files:
            with open(history_files[0], "r", encoding="utf-8") as f:
                latest_drift = json.load(f)
            severity = latest_drift.get("overall_severity", "Unknown")
            accent_map = {"Normal": "success", "Warning": "warning", "Critical": "danger"}
            render_kpi_card(
                severity,
                f"Latest Drift — {history_files[0].stem}",
                accent=accent_map.get(severity, "default"),
            )

            trend_rows = []
            for hf in history_files:
                try:
                    with open(hf, "r", encoding="utf-8") as f:
                        d = json.load(f)
                    for feat in d.get("numerical_drift", []):
                        trend_rows.append({"date": hf.stem, "feature": feat["feature"], "psi": feat["psi"]})
                except Exception:
                    pass

            if trend_rows:
                trend_df = pd.DataFrame(trend_rows)
                fig = px.line(
                    trend_df, x="date", y="psi", color="feature",
                    title="PSI Drift History",
                    color_discrete_sequence=CHART_COLORS,
                )
                fig.add_hline(y=0.10, line_dash="dash", line_color="#D97706", annotation_text="Warning")
                fig.add_hline(y=0.25, line_dash="dash", line_color="#DC2626", annotation_text="Critical")
                st.plotly_chart(apply_chart_style(fig), use_container_width=True)
        else:
            st.info("No drift history. Run `python scripts/run_drift_check.py`.")
    else:
        st.info("Drift history directory not found.")

    st.divider()

    render_section_header("Scheduled Jobs")
    scheduler_data = _safe_api_call(lambda: client._safe_get("/observability/scheduler/jobs"))
    if isinstance(scheduler_data, dict) and "error" not in scheduler_data:
        running = scheduler_data.get("scheduler_running", False)
        st.caption(f"Scheduler: {'Running' if running else 'Stopped'}")
        jobs = scheduler_data.get("jobs", [])
        if jobs:
            st.dataframe(pd.DataFrame(jobs), use_container_width=True, hide_index=True)
    else:
        st.warning("Scheduler data unavailable.")

    st.divider()

    render_section_header("Import History")
    import_log_path = BASE_DIR / "logs" / "imports.jsonl"
    if import_log_path.exists():
        imp_events = []
        with open(import_log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        imp_events.append(json.loads(line.strip()))
                    except Exception:
                        pass
        if imp_events:
            st.dataframe(pd.DataFrame(list(reversed(imp_events[-30:]))), use_container_width=True, hide_index=True)
        else:
            st.info("No ingestion events logged yet.")
    else:
        st.info("Import log not created yet.")


if __name__ == "__main__":
    render_operations_page()
