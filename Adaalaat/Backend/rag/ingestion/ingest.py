"""
RAG Ingestion — Main Script

Orchestrates the ingestion pipeline:
    1. Load documents from a source directory
    2. Chunk the documents into segments
    3. Embed each chunk
    4. Upsert into Qdrant vector store

Usage:
    python -m rag.ingestion.ingest --source ./data/legal_docs/

TODO: Implement the full ingestion pipeline.
"""

import argparse
from rag.ingestion.loaders import load_documents
from rag.embeddings import embed_documents
from database.qdrant_client import get_qdrant_client
from config import Config


# ── Chunking config ─────────────────────────────────────────────
CHUNK_SIZE = 512       # Characters per chunk
CHUNK_OVERLAP = 50     # Overlap between chunks


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split text into overlapping chunks.

    Args:
        text: Full document text
        chunk_size: Maximum characters per chunk
        overlap: Number of overlapping characters between chunks

    Returns:
        list[str]: Text chunks
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def ingest(source_dir, collection_name=None):
    """
    Run the full ingestion pipeline.

    Args:
        source_dir: Path to directory containing legal documents
        collection_name: Qdrant collection name (defaults to Config)

    TODO: Implement this function:
        1. Load documents using loaders.py
        2. Chunk each document
        3. Embed all chunks using embeddings.py
        4. Upsert into Qdrant using qdrant_client.py
    """
    if not collection_name:
        collection_name = Config.QDRANT_COLLECTION

    # Step 1: Load documents
    documents = load_documents(source_dir)
    print(f"Loaded {len(documents)} documents from {source_dir}")

    # Step 2: Chunk
    all_chunks = []
    all_metadata = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadata.append({
                "source": doc.get("source", "unknown"),
                "title": doc.get("title", ""),
                "chunk_index": i,
            })

    print(f"Created {len(all_chunks)} chunks")

    # Step 3: Embed
    vectors = embed_documents(all_chunks)
    print(f"Generated {len(vectors)} embeddings")

    # Step 4: Upsert into Qdrant
    # client = get_qdrant_client()
    # client.upsert(
    #     collection_name=collection_name,
    #     points=[
    #         PointStruct(id=i, vector=vec, payload={"text": chunk, "metadata": meta})
    #         for i, (vec, chunk, meta) in enumerate(zip(vectors, all_chunks, all_metadata))
    #     ]
    # )

    print("TODO: Upsert into Qdrant (uncomment above when Qdrant is configured)")
    print("Ingestion complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest legal documents into Qdrant")
    parser.add_argument("--source", required=True, help="Source directory with documents")
    parser.add_argument("--collection", default=None, help="Qdrant collection name")
    args = parser.parse_args()

    ingest(args.source, args.collection)
