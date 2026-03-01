"""
Local PDF Retriever

Loads a legal PDF at startup, chunks it, embeds all chunks in-memory
using HuggingFace embeddings, then performs cosine similarity search
at query time — no external vector store needed.

This replaces Qdrant for simpler deployment.
"""

import os
import logging
import numpy as np
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# ── Singleton cache ─────────────────────────────────────────────
_cached_chunks: Optional[List[Dict]] = None
_cached_embeddings: Optional[np.ndarray] = None


def _load_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file using pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"text": text, "page": i + 1})
    logger.info(f"Loaded {len(pages)} pages from {os.path.basename(pdf_path)}")
    return pages


def _chunk_pages(pages: List[Dict], chunk_size: int = 512, overlap: int = 50) -> List[Dict]:
    """
    Split page texts into overlapping chunks.

    Each chunk retains its page number for source attribution.
    """
    chunks = []
    for page in pages:
        text = page["text"]
        page_num = page["page"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_num,
                    "char_start": start,
                })
            start = end - overlap
    logger.info(f"Created {len(chunks)} chunks (size={chunk_size}, overlap={overlap})")
    return chunks


def _compute_embeddings(chunks: List[Dict]) -> np.ndarray:
    """
    Embed all chunks using the shared HuggingFace embedding model.

    Returns a numpy array of shape (num_chunks, embedding_dim).
    """
    from rag.embedding_manager import get_shared_embedding_model

    embed_model = get_shared_embedding_model()
    logger.info("Embedding chunks...")

    texts = [c["text"] for c in chunks]

    # Embed in batches to avoid OOM
    batch_size = 32
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        batch_embeddings = [embed_model.get_text_embedding(t) for t in batch]
        all_embeddings.extend(batch_embeddings)

    embeddings = np.array(all_embeddings, dtype=np.float32)
    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1  # Avoid division by zero
    embeddings = embeddings / norms

    logger.info(f"Computed {embeddings.shape[0]} embeddings (dim={embeddings.shape[1]})")
    return embeddings


def _ensure_loaded(pdf_path: str = None):
    """Load and cache the PDF chunks + embeddings on first call."""
    global _cached_chunks, _cached_embeddings

    if _cached_chunks is not None and _cached_embeddings is not None:
        return

    if pdf_path is None:
        pdf_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "legal_document.pdf"
        )

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"Legal document not found at {pdf_path}. "
            "Place your PDF at Backend/data/legal_document.pdf"
        )

    logger.info(f"Loading legal document from: {pdf_path}")
    pages = _load_pdf(pdf_path)
    _cached_chunks = _chunk_pages(pages)
    _cached_embeddings = _compute_embeddings(_cached_chunks)
    logger.info("Legal document indexed in memory ✓")


def search(query: str, top_k: int = 5, pdf_path: str = None) -> List[Dict]:
    """
    Perform cosine similarity search against the in-memory PDF embeddings.

    Args:
        query: The search query text
        top_k: Number of top results to return
        pdf_path: Optional override path to the PDF

    Returns:
        List of dicts with keys: text, page, score
    """
    _ensure_loaded(pdf_path)

    from rag.embedding_manager import get_shared_embedding_model

    embed_model = get_shared_embedding_model()

    # Embed the query
    query_embedding = np.array(
        embed_model.get_text_embedding(query), dtype=np.float32
    )
    query_norm = np.linalg.norm(query_embedding)
    if query_norm > 0:
        query_embedding = query_embedding / query_norm

    # Cosine similarity (embeddings are already normalized)
    similarities = _cached_embeddings @ query_embedding

    # Get top-k indices
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        score = float(similarities[idx])
        if score > 0.0:  # Only include positive matches
            results.append({
                "text": _cached_chunks[idx]["text"],
                "page": _cached_chunks[idx]["page"],
                "score": round(score, 4),
                "source": f"Legal Document - Page {_cached_chunks[idx]['page']}",
            })

    logger.info(f"Query: '{query[:50]}...' → {len(results)} results (top score: {results[0]['score'] if results else 0})")
    return results


def get_formatted_context(query: str, top_k: int = 2) -> str:
    """
    Convenience function: search and return formatted text context.

    Returns:
        str: Formatted context string ready for LLM consumption
    """
    results = search(query, top_k=top_k)

    if not results:
        return "No relevant legal information found in the document."

    formatted = []
    for r in results:
        formatted.append(
            f"[Source: {r['source']} | Relevance: {r['score']}]\n{r['text']}"
        )

    return "\n\n---\n\n".join(formatted)
