"""
Case Routes

Stores client advisory queries + responses so lawyers can view them as briefs.
Uses local JSON file storage (Backend/uploads/cases.json).
"""

import os
import json
import time
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify

logger = logging.getLogger(__name__)

cases_bp = Blueprint("cases", __name__)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
CASES_FILE = os.path.join(UPLOAD_DIR, "cases.json")


def _ensure_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def _load_cases():
    _ensure_dir()
    if os.path.exists(CASES_FILE):
        try:
            with open(CASES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_cases(data):
    _ensure_dir()
    with open(CASES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def store_case(query, response, client_name="Client User"):
    """Called internally by advisory route to store a case after processing."""
    cases = _load_cases()
    entry = {
        "id": str(int(time.time() * 1000)),
        "query": query,
        "client": client_name,
        "area": response.get("area", "General"),
        "analysis": response.get("analysis", ""),
        "steps": response.get("steps", []),
        "disclaimer": response.get("disclaimer", ""),
        "priority": _classify_priority(query),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    cases.append(entry)
    _save_cases(cases)
    logger.info(f"Case stored: {entry['id']} for client {client_name}")
    return entry


def _classify_priority(query):
    q = query.lower()
    high_keywords = ["evict", "termination", "fired", "fraud", "scam", "arrest", "urgent", "emergency"]
    medium_keywords = ["dispute", "complaint", "claim", "divorce", "custody"]
    if any(w in q for w in high_keywords):
        return "high"
    elif any(w in q for w in medium_keywords):
        return "medium"
    return "low"


# ── List Cases (for Lawyer Dashboard) ─────────────────────────
@cases_bp.route("/list", methods=["GET"])
def list_cases():
    """
    List all client case submissions for the lawyer.

    Query params:
        status – (optional) filter by status: pending, accepted, declined

    Returns:
        200: { "cases": [...], "total": N }
    """
    status = request.args.get("status", "").strip()
    cases = _load_cases()

    if status:
        cases = [c for c in cases if c.get("status") == status]

    # Newest first
    cases.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return jsonify({"cases": cases, "total": len(cases)}), 200


# ── Get Single Case Detail ────────────────────────────────────
@cases_bp.route("/<case_id>", methods=["GET"])
def get_case(case_id):
    """Get a single case by ID."""
    cases = _load_cases()
    case = next((c for c in cases if c.get("id") == case_id), None)
    if not case:
        return jsonify({"error": "Case not found"}), 404
    return jsonify(case), 200


# ── Update Case Status ────────────────────────────────────────
@cases_bp.route("/<case_id>/status", methods=["PATCH"])
def update_case_status(case_id):
    """
    Update case status (accept/decline).

    Body: { "status": "accepted" | "declined" }
    """
    data = request.get_json()
    new_status = data.get("status", "").strip() if data else ""

    if new_status not in ("accepted", "declined", "pending"):
        return jsonify({"error": "Invalid status"}), 400

    cases = _load_cases()
    for c in cases:
        if c.get("id") == case_id:
            c["status"] = new_status
            _save_cases(cases)
            return jsonify({"message": f"Case {new_status}", "case": c}), 200

    return jsonify({"error": "Case not found"}), 404


# ── Store Connection Request ──────────────────────────────────
@cases_bp.route("/connect", methods=["POST"])
def store_connection():
    """
    Store a connection request when a client clicks Connect on FindLawyer.

    Body: { clientName, lawyerName, lawyerId, area, query }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    cases = _load_cases()
    entry = {
        "id": str(int(time.time() * 1000)),
        "type": "connection",
        "query": data.get("query", "Connection request"),
        "client": data.get("clientName", "Client User"),
        "area": data.get("area", "General"),
        "lawyerName": data.get("lawyerName", ""),
        "lawyerId": data.get("lawyerId"),
        "analysis": f"Client {data.get('clientName', 'Client User')} has requested a consultation regarding {data.get('area', 'a legal matter')}.",
        "steps": [
            "Review the client's case details",
            "Schedule an initial consultation",
            "Prepare a fee estimate for the client",
        ],
        "disclaimer": "This is a connection request from the Adaalat platform.",
        "priority": "high",
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }
    cases.append(entry)
    _save_cases(cases)
    logger.info(f"Connection stored: {entry['client']} → {entry['lawyerName']}")

    return jsonify({"message": "Connection request stored", "id": entry["id"]}), 200
