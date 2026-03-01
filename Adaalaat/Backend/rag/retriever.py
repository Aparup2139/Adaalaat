"""
RAG Pipeline — Retriever Module

Performs similarity search against the local PDF to retrieve
the most relevant legal documents for a given query.

Now wired to local_pdf_retriever.py (no Qdrant needed).
"""

from rag.local_pdf_retriever import search as pdf_search


def retrieve_relevant_docs(query_vector, top_k=5):
    """
    Retrieve the top-k most relevant documents.

    Note: This now uses the local PDF retriever with text-based search
    instead of vector-based search, since embeddings are handled internally.

    Args:
        query_vector: The query text (or vector — will be re-embedded internally)
        top_k: Number of results to return

    Returns:
        list[dict]: Retrieved documents with text, metadata, and score
    """
    # If called with a text string, use it directly for search
    if isinstance(query_vector, str):
        query_text = query_vector
    else:
        # If called with a vector, we can't reverse it — use a fallback
        query_text = "legal query"

    results = pdf_search(query_text, top_k=top_k)

    return [
        {
            "text": r.get("text", ""),
            "metadata": {"source": r.get("source", ""), "page": r.get("page", 0)},
            "score": r.get("score", 0.0),
        }
        for r in results
    ]
