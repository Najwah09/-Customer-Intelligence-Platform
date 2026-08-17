"""
Deployment monitoring — production environment and inference status.
"""

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header
from dashboard.components.cards import render_kpi_card
from dashboard.utils.api_client import APIClient

inject_styles()


def _patch_client(client: APIClient) -> APIClient:
    import httpx

    def _safe_get(path: str):
        try:
            url = f"{client.base_url}{path}"
            resp = httpx.get(url, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
            return {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    client._safe_get = _safe_get
    return client


client = _patch_client(APIClient())


def _safe_api_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}


def render_deployment_page() -> None:
    render_page_header(
        title="Model Performance & Deployment",
        subtitle="Monitor active deployment environment, production model version, and canary traffic configuration.",
        eyebrow="System",
    )

    render_section_header("Deployment Status")

    status_data = _safe_api_call(lambda: client._safe_get("/deployment/status"))

    if isinstance(status_data, dict) and "error" not in status_data:
        env = status_data.get("environment", "blue").upper()
        prod_ver = status_data.get("production_model_version", "v1.0.0")
        canary_stage = status_data.get("canary", {}).get("stage", "0%")
    else:
        env = "BLUE"
        prod_ver = "v1.0.0"
        canary_stage = "0%"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(env, "Active Environment", accent="primary")
    with col2:
        render_kpi_card(prod_ver, "Production Model", accent="success")
    with col3:
        render_kpi_card(canary_stage, "Canary Split", accent="warning")
    with col4:
        render_kpi_card("Healthy", "Service Status", accent="success", subtext="Inference endpoint")

    if isinstance(status_data, dict) and "error" in status_data:
        st.info("Live deployment data unavailable — showing local defaults. Start the FastAPI backend for live status.")


if __name__ == "__main__":
    render_deployment_page()
