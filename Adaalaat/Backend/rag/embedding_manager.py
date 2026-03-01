"""
Embedding Manager

Uses the HuggingFace Inference API to generate embeddings remotely
via the BAAI/bge-small-en-v1.5 model. No local model download needed.
"""

import os
import json
import logging
import numpy as np
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# --- Load .env from the Backend root folder ---
# __file__ is Backend/rag/embedding_manager.py
# parent_dir is Backend/rag
# backend_dir is Backend/
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(backend_dir, ".env")
load_dotenv(dotenv_path)
# ----------------------------------------------

logger = logging.getLogger(__name__)

_hf_client = None
_model_name = None


def _get_client():
    """Get or create the singleton InferenceClient."""
    global _hf_client, _model_name

    if _hf_client is None:
        # Now this will successfully pull the token loaded from your .env file
        hf_token = os.environ.get("HUGGINGFACE_TOKEN", "") or os.environ.get("HF_TOKEN", "")
        
        if not hf_token:
            raise ValueError(
                "HUGGINGFACE_TOKEN or HF_TOKEN environment variable is required in your .env file. "
                "Get your token from https://huggingface.co/settings/tokens"
            )

        _hf_client = InferenceClient(
            provider="hf-inference",
            api_key=hf_token,
        )

        # Load model name from config
        config_path = os.path.join(backend_dir, "config.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            _model_name = config.get("embedding", {}).get(
                "model_name", "BAAI/bge-small-en-v1.5"
            )
        except FileNotFoundError:
            _model_name = "BAAI/bge-small-en-v1.5"

        logger.info(f"HF Inference Client ready (embedding: {_model_name})")

    return _hf_client, _model_name


def get_text_embedding(text: str) -> list:
    """Get embedding vector for a single text via HuggingFace Inference API."""
    client, model = _get_client()
    result = client.feature_extraction(text, model=model)

    # The API returns nested arrays — flatten to 1D
    embedding = np.array(result, dtype=np.float32)
    while embedding.ndim > 1:
        embedding = embedding[0] if embedding.shape[0] == 1 else embedding.mean(axis=0)

    return embedding.tolist()


def get_batch_embeddings(texts: list) -> list:
    """Get embeddings for a batch of texts."""
    embeddings = []
    for text in texts:
        emb = get_text_embedding(text)
        embeddings.append(emb)
    return embeddings


class HFInferenceEmbedding:
    """Wrapper class that mimics the LlamaIndex embedding interface."""

    def get_text_embedding(self, text: str) -> list:
        return get_text_embedding(text)

    def get_query_embedding(self, query: str) -> list:
        return get_text_embedding(query)


# ── Singleton accessor ──────────────────────────────────────────
_shared_embed_model = None

def get_shared_embedding_model():
    """Get a singleton embedding model that uses HF Inference API."""
    global _shared_embed_model
    if _shared_embed_model is None:
        _get_client()
        _shared_embed_model = HFInferenceEmbedding()
        logger.info("Shared HF Inference embedding model ready")
    return _shared_embed_model