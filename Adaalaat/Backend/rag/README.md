# RAG Pipeline — Embeddings

This module handles converting text into vector embeddings for semantic search.

## Setup Instructions

1. Choose an embedding model:
   - **Sentence Transformers** (local): `all-MiniLM-L6-v2` or `legal-bert-base-uncased`
   - **OpenAI Embeddings** (API): `text-embedding-3-small`

2. Install the chosen library (already in requirements.txt):
   ```bash
   pip install sentence-transformers
   # or for OpenAI
   pip install openai
   ```

3. Implement the `embed_query()` and `embed_documents()` functions in `embeddings.py`

4. The embedding dimension must match your **Qdrant collection** configuration.

## Integration Points

- `embeddings.py` → called by `services/advisory_service.py` and `services/document_service.py`
- Output vectors → fed into `retriever.py` for Qdrant similarity search
