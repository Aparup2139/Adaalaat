from flask import Blueprint, request, jsonify
from services.document_service import DocumentService

documents_bp = Blueprint("documents", __name__)


@documents_bp.route("/draft", methods=["POST"])
def generate_draft():
    """
    Generate a legal document draft using RAG.

    The system retrieves relevant templates and legal context from the
    vector store, then uses the LLM to generate a tailored document draft.
    The lawyer can then review, edit, and sign it offline.

    Request body:
    {
        "caseId": "case-uuid",
        "lawyerId": "lawyer-uuid",
        "documentType": "Legal Notice" | "Appeal Letter" | "Affidavit" | ...,
        "context": "Brief description of what the document should address"
    }

    Returns:
        200: {
            "documentId": "doc-uuid",
            "title": "Legal Notice – Tenant Eviction",
            "content": "DRAFT CONTENT...",
            "documentType": "Legal Notice",
            "status": "draft",
            "createdAt": "2026-03-01T00:00:00Z"
        }
        400: { "error": "..." }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required = ["lawyerId", "documentType", "context"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    result, error = DocumentService.generate_draft(
        case_id=data.get("caseId"),
        lawyer_id=data["lawyerId"],
        document_type=data["documentType"],
        context=data["context"],
    )
    if error:
        return jsonify({"error": error}), 500

    return jsonify(result), 200


@documents_bp.route("", methods=["GET"])
def list_documents():
    """
    List documents for a user (client or lawyer).

    Query params:
        userId – The user's ID
        role   – "client" or "lawyer"
        status – Filter by status: "draft", "sent", "completed" (optional)

    Returns:
        200: {
            "documents": [ { "id", "title", "type", "status", "date", ... } ],
            "total": 5
        }
    """
    user_id = request.args.get("userId", "")
    role = request.args.get("role", "")
    status = request.args.get("status", "")

    if not user_id:
        return jsonify({"error": "userId query parameter is required"}), 400

    result, error = DocumentService.list_documents(
        user_id=user_id,
        role=role,
        status=status,
    )
    if error:
        return jsonify({"error": error}), 500

    return jsonify(result), 200


@documents_bp.route("/<string:doc_id>/send", methods=["POST"])
def send_document(doc_id):
    """
    Lawyer sends a signed document PDF directly to the client.

    The lawyer has already reviewed and signed the draft offline.
    This endpoint records the delivery and notifies the client.

    Request body:
    {
        "lawyerId": "lawyer-uuid",
        "clientId": "client-uuid",
        "notes": "Please review and sign page 3"  (optional)
    }

    Returns:
        200: { "message": "Document sent successfully", "documentId": "..." }
        400: { "error": "..." }
    """
    data = request.get_json()

    if not data or not data.get("lawyerId") or not data.get("clientId"):
        return jsonify({"error": "lawyerId and clientId are required"}), 400

    result, error = DocumentService.send_document(
        doc_id=doc_id,
        lawyer_id=data["lawyerId"],
        client_id=data["clientId"],
        notes=data.get("notes", ""),
    )
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Document sent successfully", **result}), 200
