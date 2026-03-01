"""
RAG Ingestion — Document Loaders

Loads legal documents from various file formats into a standard structure.

Supported formats:
    - .txt  (plain text)
    - .pdf  (via PyPDF2 or pdfplumber)
    - .html (stripped of tags)

TODO: Implement PDF loading (add PyPDF2 or pdfplumber to requirements.txt).
"""

import os
import glob


def load_documents(source_dir):
    """
    Load all documents from a directory.

    Args:
        source_dir: Path to directory containing documents

    Returns:
        list[dict]: Each dict has keys:
            - "text": The document content
            - "source": File path
            - "title": Filename without extension
    """
    documents = []

    # Find all supported files
    patterns = ["*.txt", "*.pdf", "*.html", "*.md"]
    for pattern in patterns:
        for filepath in glob.glob(os.path.join(source_dir, "**", pattern), recursive=True):
            doc = load_single_document(filepath)
            if doc:
                documents.append(doc)

    return documents


def load_single_document(filepath):
    """
    Load a single document based on its file extension.

    Args:
        filepath: Path to the document

    Returns:
        dict with text, source, title — or None if unsupported
    """
    ext = os.path.splitext(filepath)[1].lower()
    title = os.path.splitext(os.path.basename(filepath))[0]

    try:
        if ext == ".txt" or ext == ".md":
            return load_text(filepath, title)
        elif ext == ".pdf":
            return load_pdf(filepath, title)
        elif ext == ".html":
            return load_html(filepath, title)
        else:
            return None
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def load_text(filepath, title):
    """Load a plain text or markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return {"text": text, "source": filepath, "title": title}


def load_pdf(filepath, title):
    """
    Load a PDF file.

    TODO: Implement with PyPDF2 or pdfplumber:
        pip install PyPDF2
        # or
        pip install pdfplumber
    """
    # Placeholder — requires PyPDF2 or pdfplumber
    # import PyPDF2
    # reader = PyPDF2.PdfReader(filepath)
    # text = "\n".join(page.extract_text() or "" for page in reader.pages)
    # return {"text": text, "source": filepath, "title": title}

    print(f"PDF loading not implemented yet: {filepath}")
    return None


def load_html(filepath, title):
    """Load an HTML file, stripping tags."""
    import re
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return {"text": text, "source": filepath, "title": title}
