from flask import Blueprint, request, jsonify
from services.advisory_service import AdvisoryService

advisory_bp = Blueprint("advisory", __name__)


@advisory_bp.route("/query", methods=["POST"])
def submit_query():
    """
    Submit a legal query for AI-powered advisory.

    Workflow:
        1. Receive client's legal query text
        2. Embed the query into a vector
        3. Retrieve top-k relevant legal documents from Qdrant
        4. Synthesize query + context via LLM (RAG generation)
        5. Return preliminary advisory report with disclaimer

    Request body:
    {
        "query": "I am facing a tenant eviction dispute...",
        "userId": "user-uuid"  (optional, for session tracking)
    }

    Returns:
        200: {
            "area": "Tenancy & Property Law",
            "analysis": "Based on your description...",
            "steps": ["Step 1...", "Step 2..."],
            "relevantStatutes": ["Section 106 TPA", ...],
            "disclaimer": "This is AI-generated..."
        }
        400: { "error": "..." }
    """
    data = request.get_json()

    if not data or not data.get("query"):
        return jsonify({"error": "Legal query text is required"}), 400

    query_text = data["query"].strip()
    if len(query_text) < 10:
        return jsonify({"error": "Please provide a more detailed description of your situation"}), 400

    user_id = data.get("userId")
    history = data.get("history", [])  # Chat history for multi-turn context
    client_name = data.get("clientName", "Client User")

    result, error = AdvisoryService.process_query(
        query_text, user_id=user_id, history=history
    )
    if error:
        return jsonify({"error": error}), 500

    # Store the case for the Lawyer Dashboard
    try:
        from routes.case_routes import store_case
        store_case(query_text, result, client_name=client_name)
    except Exception:
        pass  # Non-critical — don't fail the response

    return jsonify(result), 200
