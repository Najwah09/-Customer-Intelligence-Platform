"""
AI Analyst — natural language query interface for retention intelligence.
"""

import streamlit as st

from dashboard.components.layout import inject_styles, render_page_header, render_section_header
from backend.services.ai_agent_engine import ai_agent
from backend.services.llm_provider import llm_service

inject_styles()

SUGGESTED_PROMPTS = [
    "Which high-risk customers should I prioritize?",
    "Why are customers churning?",
    "Which segment has the highest churn?",
    "What is the average LTV?",
]


def render_ai_retention_agent_page():
    import importlib
    import backend.services.ai_agent_engine
    importlib.reload(backend.services.ai_agent_engine)
    from backend.services.ai_agent_engine import ai_agent

    render_page_header(
        title="AI Analyst",
        subtitle="Ask questions about customers, churn, LTV, segments, and retention opportunities.",
        eyebrow="AI",
    )


    # ------------------------------------------------------------------
    # Sidebar LLM Engine Status & Credentials Control
    # ------------------------------------------------------------------
    with st.sidebar:
        st.subheader("🤖 Real LLM Provider Settings")
        
        gemini_status = (
            llm_service.check_gemini_health()
            if hasattr(llm_service, "check_gemini_health")
            else {"status": "OFFLINE"}
        )
        ollama_active = (
            llm_service.check_ollama_available()
            if hasattr(llm_service, "check_ollama_available")
            else False
        )
        groq_active = bool(getattr(llm_service, "groq_api_key", ""))


        if gemini_status.get("status") == "CONNECTED":
            st.success(f"🟢 Active: Google Gemini API ({gemini_status.get('model')})")
        elif ollama_active:
            st.success(f"🟢 Active: Local Ollama ({llm_service.ollama_model})")
        elif groq_active:
            st.success("🟢 Active: Groq API (llama-3.1-8b-instant)")
        else:
            st.info("⚡ Active: Grounded Reasoning Engine (< 50ms)")

        with st.expander("⚙️ Configure LLM Provider / API Keys"):
            gemini_input = st.text_input(
                "Google Gemini API Key",
                value=llm_service.gemini_api_key,
                type="password",
                help="Get your key at https://aistudio.google.com/app/apikey",
            )
            groq_input = st.text_input(
                "Groq API Key (Free)",
                value=llm_service.groq_api_key,
                type="password",
                help="Get a free instant key at https://console.groq.com",
            )
            ollama_url_input = st.text_input(
                "Ollama URL",
                value=llm_service.ollama_url,
                help="Local Ollama server address (default: http://localhost:11434)",
            )
            ollama_model_input = st.selectbox(
                "Ollama Model Name",
                options=["llama3", "mistral", "phi3", "gemma", "qwen"],
                index=0,
            )

            if st.button("Save & Apply LLM Settings", use_container_width=True):
                llm_service.update_credentials(
                    gemini_key=gemini_input.strip(),
                    groq_key=groq_input.strip(),
                    ollama_url=ollama_url_input.strip(),
                    ollama_model=ollama_model_input.strip(),
                )
                st.success("LLM Provider settings updated!")
                st.rerun()


    # ------------------------------------------------------------------
    # Suggested Prompts UI
    # ------------------------------------------------------------------
    render_section_header("Suggested prompts")

    prompt_cols = st.columns(len(SUGGESTED_PROMPTS))
    selected_prompt = None
    for col, prompt in zip(prompt_cols, SUGGESTED_PROMPTS):
        with col:
            if st.button(prompt, use_container_width=True):
                selected_prompt = prompt

    st.divider()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I'm your Customer Intelligence Analyst. I can help you investigate customer churn, "
                    "lifetime value, segment performance, what-if retention simulations, and strategic priorities. "
                    "Ask a question or select a suggested prompt above."
                ),
                "citations": [],
            }
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("citations"):
                sources = ", ".join(msg["citations"])
                engine_tag = f" · Engine: {msg['llm_engine']}" if msg.get("llm_engine") else ""
                st.caption(f"Analysis basis: **{sources}**{engine_tag}")

    # Interactive Human Approval Card
    state = ai_agent.get_session_state()
    if state.last_generated_message and state.pending_action:
        st.divider()
        st.subheader("🛠️ Human Approval & Action Execution Panel")
        col_rev, col_friendly, col_send = st.columns(3)
        with col_rev:
            if st.button("🔍 Review Customer Offer", use_container_width=True):
                st.info(f"Target Account: #{state.last_generated_message.get('customer_id')} · Strategy: {state.last_generated_message.get('recommended_action')}")
        with col_friendly:
            if st.button("😊 Make Tone Friendly", use_container_width=True):
                res = ai_agent.process_natural_language_query("make it friendly")
                st.session_state.chat_history.append({"role": "assistant", "content": res["response"], "citations": res.get("citations", []), "llm_engine": res.get("llm_engine", "Grounded Analyst Engine")})
                st.rerun()
        with col_send:
            if st.button("✅ Approve & Send Campaign", type="primary", use_container_width=True):
                res = ai_agent.process_natural_language_query("send it")
                st.session_state.chat_history.append({"role": "assistant", "content": res["response"], "citations": res.get("citations", []), "llm_engine": res.get("llm_engine", "Grounded Analyst Engine")})
                st.rerun()

    user_input = st.chat_input("Ask about churn, LTV, segments, or retention strategies…")
    if selected_prompt:
        user_input = selected_prompt

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input, "citations": []})

        with st.spinner("Analyzing portfolio intelligence…"):
            res = ai_agent.process_natural_language_query(user_input)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": res["response"],
            "citations": res.get("citations", []),
            "llm_engine": res.get("llm_engine", "Google Gemini API (gemini-flash)"),
        })

        st.rerun()



if __name__ == "__main__":
    render_ai_retention_agent_page()
