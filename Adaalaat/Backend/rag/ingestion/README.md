# RAG Ingestion Pipeline

This directory contains the data ingestion pipeline for loading legal documents
into the Qdrant vector store.

## Overview

The ingestion pipeline:
1. **Loads** raw legal documents (PDFs, text files, HTML) via document loaders
2. **Chunks** the documents into manageable segments
3. **Embeds** each chunk into a dense vector using the embedding model
4. **Stores** the vectors + metadata into the Qdrant collection

## Files

| File | Purpose |
|---|---|
| `ingest.py` | Main ingestion script — orchestrates the full pipeline |
| `loaders.py` | Document loaders for PDF, text, and HTML files |

## Usage

```bash
# From the Backend/ directory
python -m rag.ingestion.ingest --source ./data/legal_docs/ --collection legal_documents
```

## Data Sources

Place your legal documents in a `data/` directory:
```
Backend/
├── data/
│   ├── statutes/         # Indian legal statutes (IPC, CPC, etc.)
│   ├── case_law/         # Relevant case law documents
│   └── templates/        # Legal document templates
```

## Configuration

- Embedding model: Configured in `rag/embeddings.py`
- Qdrant connection: Configured in `database/qdrant_client.py`
- Collection name: Set in `.env` as `QDRANT_COLLECTION`
- Chunk size / overlap: Configurable in `ingest.py`
