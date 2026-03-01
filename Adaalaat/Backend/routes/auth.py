from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Register a new user (client or lawyer).

    Request body:
    {
        "email": "user@example.com",
        "password": "securepassword",
        "fullName": "John Doe",
        "phone": "+91 98765 43210",
        "role": "client" | "lawyer",
        // Lawyer-only fields:
        "barRegistration": "BCI/MAH/12345/2020",  (optional, required for lawyer)
        "portfolioUrl": "https://portfolio.com"     (optional, required for lawyer)
    }

    Returns:
        201: { "message": "User created", "user": { ... }, "token": "..." }
        400: { "error": "..." }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required = ["email", "password", "fullName", "role"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if data["role"] not in ("client", "lawyer"):
        return jsonify({"error": "Role must be 'client' or 'lawyer'"}), 400

    if data["role"] == "lawyer":
        if not data.get("barRegistration"):
            return jsonify({"error": "Bar registration number is required for lawyers"}), 400
        if not data.get("portfolioUrl"):
            return jsonify({"error": "Portfolio URL is required for lawyers"}), 400

    result, error = AuthService.signup(data)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "User created successfully", **result}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user.

    Request body:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }

    Returns:
        200: { "message": "Login successful", "user": { ... }, "token": "..." }
        401: { "error": "Invalid credentials" }
    """
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    result, error = AuthService.login(data["email"], data["password"])
    if error:
        return jsonify({"error": error}), 401

    return jsonify({"message": "Login successful", **result}), 200
