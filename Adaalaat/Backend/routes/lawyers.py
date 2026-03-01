from flask import Blueprint, request, jsonify
from services.lawyer_service import LawyerService

lawyers_bp = Blueprint("lawyers", __name__)


@lawyers_bp.route("/search", methods=["GET"])
def search_lawyers():
    """
    Search for lawyers by legal domain, location, or availability.

    Query params:
        domain   – Legal area (e.g., "Tenancy & Property Law")
        location – City or region (optional)
        page     – Page number for pagination (default 1)
        limit    – Results per page (default 10)

    Returns:
        200: {
            "lawyers": [ { "id", "name", "domain", "location", "rating", ... } ],
            "total": 42,
            "page": 1
        }
    """
    domain = request.args.get("domain", "")
    location = request.args.get("location", "")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    result, error = LawyerService.search(
        domain=domain,
        location=location,
        page=page,
        limit=limit,
    )
    if error:
        return jsonify({"error": error}), 500

    return jsonify(result), 200


@lawyers_bp.route("/<string:lawyer_id>", methods=["GET"])
def get_lawyer_profile(lawyer_id):
    """
    Get a specific lawyer's profile details.

    Returns:
        200: { "id", "name", "domain", "barRegistration", "bio", "rating", ... }
        404: { "error": "Lawyer not found" }
    """
    lawyer, error = LawyerService.get_profile(lawyer_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(lawyer), 200


@lawyers_bp.route("/<string:lawyer_id>/book", methods=["POST"])
def book_consultation(lawyer_id):
    """
    Request a consultation with a lawyer.

    Request body:
    {
        "clientId": "client-uuid",
        "caseId": "case-uuid",
        "message": "Brief description of what I need help with",
        "preferredDate": "2026-03-05"  (optional)
    }

    Returns:
        201: { "message": "Consultation requested", "bookingId": "..." }
        400: { "error": "..." }
    """
    data = request.get_json()

    if not data or not data.get("clientId"):
        return jsonify({"error": "Client ID is required"}), 400

    result, error = LawyerService.book_consultation(
        lawyer_id=lawyer_id,
        client_id=data["clientId"],
        case_id=data.get("caseId"),
        message=data.get("message", ""),
        preferred_date=data.get("preferredDate"),
    )
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Consultation requested successfully", **result}), 201
