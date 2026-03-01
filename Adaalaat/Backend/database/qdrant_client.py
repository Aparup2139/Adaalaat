"""
Qdrant Client

Initializes and provides a singleton Qdrant client for vector store
operations (document embedding storage and similarity search).

Required environment variables:
    QDRANT_URL     — Qdrant server URL (default: http://localhost:6333)
    QDRANT_API_KEY — API key for Qdrant Cloud (optional for local)
    QDRANT_COLLECTION — Collection name (default: legal_documents)

Collection Setup:
    Before using, create the collection in Qdrant with the correct vector
    dimension matching your embedding model:

    - all-MiniLM-L6-v2: 384 dimensions
    - text-embedding-3-small: 1536 dimensions
    - legal-bert-base-uncased: 768 dimensions

    Example (using qdrant_client):
        from qdrant_client.models import Distance, VectorParams

        client.create_collection(
            collection_name="legal_documents",
            vectors_config=VectorParams(
                size=384,  # Match your embedding model
                distance=Distance.COSINE,
            ),
        )
"""

from config import Config

_qdrant_client = None


def get_qdrant_client():
    """
    Get or create the singleton Qdrant client.

    Returns:
        qdrant_client.QdrantClient — The initialized client

    Raises:
        ValueError if QDRANT_URL is not set
    """
    global _qdrant_client

    if _qdrant_client is None:
        if not Config.QDRANT_URL:
            raise ValueError(
                "QDRANT_URL must be set in .env. "
                "For local: http://localhost:6333, "
                "For cloud: your Qdrant Cloud endpoint."
            )

        from qdrant_client import QdrantClient

        if Config.QDRANT_API_KEY:
            _qdrant_client = QdrantClient(
                url=Config.QDRANT_URL,
                api_key=Config.QDRANT_API_KEY,
            )
        else:
            _qdrant_client = QdrantClient(url=Config.QDRANT_URL)

    return _qdrant_client
