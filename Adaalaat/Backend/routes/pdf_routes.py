"""
PDF Upload & Download Routes

Handles file upload from lawyers, listing for clients, and serving PDFs.
Files are stored locally in Backend/uploads/ with metadata in a JSON file.
"""

import os
import json
import time
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

pdf_bp = Blueprint("pdf", __name__)

# ── Config ──────────────────────────────────────────────────────
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
METADATA_FILE = os.path.join(UPLOAD_DIR, "metadata.json")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _ensure_upload_dir():
    """Create upload directory if it doesn't exist."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def _load_metadata():
    """Load metadata from JSON file."""
    _ensure_upload_dir()
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_metadata(data):
    """Save metadata to JSON file."""
    _ensure_upload_dir()
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Upload PDF ──────────────────────────────────────────────────
@pdf_bp.route("/upload", methods=["POST"])
def upload_pdf():
    """
    Upload a PDF from a lawyer to a specific client.

    Form data:
        file     – The PDF file
        client   – Client name (e.g. "Rajeev Mehta")
        lawyer   – Lawyer name (e.g. "Adv. Arjun Khanna")
        notes    – Optional notes

    Returns:
        200: { "message": "...", "filename": "...", "id": "..." }
        400: { "error": "..." }
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    client = request.form.get("client", "").strip()
    lawyer = request.form.get("lawyer", "Adv. Arjun Khanna").strip()
    notes = request.form.get("notes", "").strip()

    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not client:
        return jsonify({"error": "Client name is required"}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        return jsonify({"error": "File exceeds 10MB limit"}), 400

    # Generate unique filename
    _ensure_upload_dir()
    original_name = secure_filename(file.filename)
    timestamp = int(time.time())
    stored_name = f"{timestamp}_{original_name}"
    file_path = os.path.join(UPLOAD_DIR, stored_name)

    file.save(file_path)
    logger.info(f"PDF saved: {stored_name} (for client: {client})")

    # Store metadata
    metadata = _load_metadata()
    entry = {
        "id": str(timestamp),
        "original_name": original_name,
        "stored_name": stored_name,
        "client": client,
        "lawyer": lawyer,
        "notes": notes,
        "size_bytes": size,
        "uploaded_at": datetime.now().isoformat(),
        "status": "delivered",
    }
    metadata.append(entry)
    _save_metadata(metadata)

    return jsonify({
        "message": "PDF uploaded successfully",
        "filename": stored_name,
        "id": entry["id"],
        "original_name": original_name,
    }), 200


# ── List PDFs for a Client ──────────────────────────────────────
@pdf_bp.route("/list", methods=["GET"])
def list_pdfs():
    """
    List PDFs sent to a specific client.

    Query params:
        client – The client's name
        lawyer – (optional) Filter by lawyer name

    Returns:
        200: { "documents": [...], "total": N }
    """
    client = request.args.get("client", "").strip()
    lawyer = request.args.get("lawyer", "").strip()

    metadata = _load_metadata()

    # Filter by client (case-insensitive)
    filtered = [
        m for m in metadata
        if m.get("client", "").lower() == client.lower()
    ] if client else metadata

    # Optionally filter by lawyer
    if lawyer:
        filtered = [
            m for m in filtered
            if m.get("lawyer", "").lower() == lawyer.lower()
        ]

    # Sort by upload time (newest first)
    filtered.sort(key=lambda x: x.get("uploaded_at", ""), reverse=True)

    documents = []
    for m in filtered:
        documents.append({
            "id": m.get("id"),
            "name": m.get("original_name"),
            "storedName": m.get("stored_name"),
            "lawyer": m.get("lawyer"),
            "client": m.get("client"),
            "notes": m.get("notes", ""),
            "size": m.get("size_bytes", 0),
            "date": m.get("uploaded_at", ""),
            "status": m.get("status", "delivered"),
        })

    return jsonify({"documents": documents, "total": len(documents)}), 200


# ── Download / Serve PDF ────────────────────────────────────────
@pdf_bp.route("/download/<path:filename>", methods=["GET"])
def download_pdf(filename):
    """
    Serve a PDF file for viewing or download.

    Args:
        filename – The stored filename (with timestamp prefix)

    Returns:
        The PDF file, or 404 if not found.
    """
    safe_name = secure_filename(filename)
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(UPLOAD_DIR, safe_name, as_attachment=False)
