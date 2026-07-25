"""
API Client to communicate with Agrisensa AI Core (FastAPI).
Handles Agentic RAG chat and ML endpoints.
"""
import os
import requests
import logging
from typing import List, Dict, Any

logger = logging.getLogger("streamlit.api_core")

# Get from env, fallback to localhost
BASE_URL = os.environ.get("API_CORE_BASE_URL", "http://localhost:8080")

def chat_with_agent(query: str, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Sends a message to the AI Core Smart Agent.
    """
    url = f"{BASE_URL}/api/chat"
    payload = {
        "query": query,
        "chat_history": chat_history
    }
    
    try:
        response = requests.post(url, json=payload, timeout=45)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with AI Core: {e}")
        return {
            "answer": f"⚠️ Maaf, terjadi kesalahan saat menghubungi AI Core Server. Pastikan server AI berjalan di {BASE_URL}. Detail: {str(e)}"
        }

def get_health() -> Dict[str, Any]:
    """Check health of the AI Core."""
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"status": "error"}
    except Exception:
        return {"status": "unreachable"}
