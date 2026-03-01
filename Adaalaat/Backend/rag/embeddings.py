"""
RAG Pipeline — Embeddings Module

Converts text into dense vector embeddings for semantic search.
Now wired directly to embedding_manager.py to use HuggingFace Inference API.
"""

# Import the actual working functions from your embedding_manager
from rag.embedding_manager import get_text_embedding, get_batch_embeddings

def embed_query(text: str) -> list:
    """
    Convert a query string into a vector embedding.

    Args:
        text: The input text to embed

    Returns:
        list[float]: A dense vector
    """
    # Call the manager function that uses your .env token
    return get_text_embedding(text)


def embed_documents(texts: list) -> list:
    """
    Convert a batch of document strings into vector embeddings.

    Args:
        texts: list[str] — The documents to embed

    Returns:
        list[list[float]]: A list of dense vectors
    """
    # Call the manager function that uses your .env token
    return get_batch_embeddings(texts)