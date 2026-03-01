import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

    # HuggingFace Inference API
    HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "") or os.getenv("HF_TOKEN", "")

    # LLM Model
    LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
