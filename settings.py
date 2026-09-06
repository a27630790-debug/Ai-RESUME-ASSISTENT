import os

# Detect if we are running inside Google Colab
try:
    from google.colab import userdata  # type: ignore
    IN_COLAB = True
except ImportError:
    IN_COLAB = False


def get_secret(key: str) -> str:
    """
    Universal secret loader.
    Priority order:
      1. Google Colab Secrets   (Colab -> key icon on left sidebar)
      2. Streamlit Secrets      (used later when deployed on Streamlit Cloud)
      3. Environment variable   (used for local/dev testing)

    NEVER hardcode actual key values here. Only key NAMES are defined below.
    """
    if IN_COLAB:
        try:
            val = userdata.get(key)
            if val:
                return val
        except Exception:
            pass  # secret not set in Colab, fall through

    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass  # not running inside streamlit, or secret not set

    return os.environ.get(key, "")


# ============================================================
# 🔑 API KEY NAMES — put actual key VALUES in Colab Secrets /
# Streamlit Secrets, never directly in this file.
# ============================================================
GEMINI_API_KEY_NAME = "GEMINI_API_KEY"   # <-- Colab: add secret named exactly this
GROQ_API_KEY_NAME = "GROQ_API_KEY"       # <-- Colab: add secret named exactly this

# Model names — change here if you want to switch models later
GEMINI_MODEL = "gemini-2.0-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Fallback order: Gemini tried first, Groq if Gemini fails/unavailable
PROVIDER_FALLBACK_ORDER = ["gemini", "groq"]
