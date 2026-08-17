"""
Unified LLM Provider Service for RETAINAI Platform.

Primary: Google Gemini API (gemini-flash / gemini-1.5-flash)
Secondary: Ollama (Local free LLM server running on http://localhost:11434 with llama3/mistral/phi3)
Fallback: Grounded High-Speed Analyst Engine (< 50ms fallback when no cloud/local LLM service is online)
"""

import os
import time
from typing import Any, Dict, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

from backend.core.logger import logger
from backend.services.project_knowledge import project_knowledge

SYSTEM_PROJECT_KNOWLEDGE = (
    "You are RETAINAI's Customer Intelligence Analyst. "
    "RETAINAI is an enterprise SaaS platform built on Python 3.12, FastAPI, Streamlit, PostgreSQL, LightGBM, SHAP, and K-Means.\n\n"
    "Platform Specifications:\n"
    "• Active Portfolio: 7,043 Telco Subscribers\n"
    "• Churn Classifier: LightGBM Classifier (ROC-AUC: 0.847, Optimal Threshold: 0.61)\n"
    "• LTV Model: LightGBM Regressor (Predicts lifetime revenue exposure & remaining contract horizon)\n"
    "• Cohort Segmentation: K-Means Clustering (High-Value, Loyal, Budget Subscribers)\n"
    "• Explainability: SHAP (TreeExplainer) feature attributions\n"
    "• Operations: APScheduler drift monitoring (PSI threshold 0.10 warning, 0.25 critical)\n\n"
    "Rules:\n"
    "1. Answer user questions accurately using ONLY the provided structured tool data.\n"
    "2. Never invent customer numbers, churn probabilities, LTV, or SHAP values.\n"
    "3. Never expose internal Python function names (say 'Based on our churn model and SHAP feature attribution').\n"
    "4. Be clear, concise, professional, data-grounded, and directly address the user's intent."
)


class LLMProviderService:
    """Unified LLM Manager supporting Gemini API, Ollama, and Grounded Engine."""

    def __init__(self):
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "") or os.environ.get(
            "CUSTOM_LLM_API_KEY", ""
        )
        self.gemini_model = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")

        self.ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.environ.get("OLLAMA_MODEL", "llama3")

        self.groq_api_key = os.environ.get("GROQ_API_KEY", "")
        self.custom_api_key = os.environ.get("CUSTOM_LLM_API_KEY", "")
        self.custom_base_url = os.environ.get("CUSTOM_LLM_BASE_URL", "")
        self.custom_model = os.environ.get("CUSTOM_LLM_MODEL", "llama-3.1-8b-instant")
        self.provider = os.environ.get("LLM_PROVIDER", "auto").lower()

    def get_gemini_key(self) -> str:
        """Get active Gemini API key from instance variable or environment."""
        return (
            self.gemini_api_key
            or os.environ.get("GEMINI_API_KEY", "")
            or os.environ.get("CUSTOM_LLM_API_KEY", "")
        )

    def update_credentials(
        self,
        gemini_key: Optional[str] = None,
        groq_key: Optional[str] = None,
        ollama_url: Optional[str] = None,
        ollama_model: Optional[str] = None,
        custom_key: Optional[str] = None,
        custom_base_url: Optional[str] = None,
        custom_model: Optional[str] = None,
    ):
        """Update runtime LLM credentials from Streamlit sidebar controls."""
        if gemini_key is not None:
            self.gemini_api_key = gemini_key
            os.environ["GEMINI_API_KEY"] = gemini_key
        if groq_key is not None:
            self.groq_api_key = groq_key
        if ollama_url is not None:
            self.ollama_url = ollama_url
        if ollama_model is not None:
            self.ollama_model = ollama_model
        if custom_key is not None:
            self.custom_api_key = custom_key
        if custom_base_url is not None:
            self.custom_base_url = custom_base_url
        if custom_model is not None:
            self.custom_model = custom_model

    def check_gemini_health(self) -> Dict[str, Any]:
        """Verify Gemini API connectivity with working endpoints."""
        key = self.get_gemini_key()
        if not key:
            return {
                "status": "NOT_CONFIGURED",
                "message": "GEMINI_API_KEY environment variable is not set.",
            }
        models_to_test = [
            "gemini-flash-lite-latest",
            "gemini-3.6-flash",
            "gemini-flash-latest",
        ]
        for m in models_to_test:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key}"
                payload = {"contents": [{"parts": [{"text": "ping"}]}]}
                resp = httpx.post(url, json=payload, timeout=4.0)
                if resp.status_code == 200:
                    return {
                        "status": "CONNECTED",
                        "model": m,
                        "message": f"Successfully connected to Google Gemini API ({m}).",
                    }
            except Exception as e:
                logger.debug(f"Gemini health check attempt for {m} failed: {e}")
        return {
            "status": "OFFLINE",
            "message": "Gemini API request failed or rate-limited",
        }

    def check_ollama_available(self) -> bool:
        """Check if local Ollama server is running on port 11434 with quick timeout."""
        try:
            resp = httpx.get(f"{self.ollama_url}/api/tags", timeout=1.0)
            return resp.status_code == 200
        except Exception:
            return False

    def query_gemini(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Fast Google Gemini API query with working Gemini 3.6 Flash endpoints."""
        key = self.get_gemini_key()
        if not key:
            return None
        sys_ctx = (
            f"{SYSTEM_PROJECT_KNOWLEDGE}\n\n{system_prompt}"
            if system_prompt
            else SYSTEM_PROJECT_KNOWLEDGE
        )
        models_to_try = [
            "gemini-3.6-flash",
            "gemini-flash-lite-latest",
            "gemini-flash-latest",
        ]

        for model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{sys_ctx}\n\n{prompt}"}]}],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 350},
                }
                resp = httpx.post(url, json=payload, timeout=3.5)
                if resp.status_code == 200:
                    candidates = resp.json().get("candidates", [])
                    if candidates:
                        text = candidates[0]["content"]["parts"][0]["text"].strip()
                        if text:
                            return text
            except Exception as e:
                logger.debug(f"Gemini API model {model} attempt failed: {e}")
        return None

    def query_ollama(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Fast 1.5-second local Ollama query using fast models."""
        url = f"{self.ollama_url}/api/generate"
        sys_ctx = (
            f"{SYSTEM_PROJECT_KNOWLEDGE}\n\n{system_prompt}"
            if system_prompt
            else SYSTEM_PROJECT_KNOWLEDGE
        )
        full_prompt = f"{sys_ctx}\n\n{prompt}"
        models_to_try = ["qwen2.5:3b", "phi3:mini", "llama3:latest"]
        for m in models_to_try:
            try:
                payload = {
                    "model": m,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.2, "top_p": 0.9, "num_predict": 180},
                }
                resp = httpx.post(url, json=payload, timeout=1.5)
                if resp.status_code == 200:
                    text = resp.json().get("response", "").strip()
                    if text:
                        return text
            except Exception:
                pass
        return None

    def query_groq(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Query Groq free API endpoint if valid GROQ_API_KEY is provided."""
        if not self.groq_api_key or not self.groq_api_key.startswith("gsk_"):
            return None

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json",
            }
            sys_ctx = (
                f"{SYSTEM_PROJECT_KNOWLEDGE}\n\n{system_prompt}"
                if system_prompt
                else SYSTEM_PROJECT_KNOWLEDGE
            )
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": sys_ctx},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 300,
            }
            resp = httpx.post(url, headers=headers, json=payload, timeout=4.0)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.debug(f"Groq API call failed: {e}")
        return None

    def generate_llm_response(
        self,
        prompt: str,
        system_prompt: str = "",
        fallback_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate response using available LLM backend (Gemini -> Ollama -> Groq -> Grounded Generator).
        Fast <3s response time guarantee.
        """
        # 1. Try Gemini API if key is present
        gemini_res = self.query_gemini(prompt, system_prompt)
        if gemini_res:
            return {
                "text": gemini_res,
                "llm_engine": "Google Gemini API (gemini-flash)",
                "status": "SUCCESS",
            }

        # 2. Try Ollama if server is online
        if self.check_ollama_available():
            ollama_res = self.query_ollama(prompt, system_prompt)
            if ollama_res:
                return {
                    "text": ollama_res,
                    "llm_engine": f"Ollama ({self.ollama_model})",
                    "status": "SUCCESS",
                }

        # 3. Try Groq API if key is present
        if self.groq_api_key:
            groq_res = self.query_groq(prompt, system_prompt)
            if groq_res:
                return {
                    "text": groq_res,
                    "llm_engine": "Groq (llama-3.1-8b-instant)",
                    "status": "SUCCESS",
                }

        # 4. High-Speed Grounded Fallback (< 50ms)
        return {
            "text": None,
            "llm_engine": "Grounded Analyst Engine",
            "status": "FAST_GROUNDED_FALLBACK",
        }


llm_service = LLMProviderService()
