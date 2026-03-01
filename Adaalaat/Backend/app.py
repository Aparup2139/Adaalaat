from flask import Flask, jsonify
from flask_cors import CORS
from config import Config


def create_app():
    """Application factory — creates and configures the Flask app."""

    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for the Vite dev server
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

    # ── Register Blueprints ─────────────────────────────────────
    from routes.auth import auth_bp
    from routes.advisory import advisory_bp
    from routes.lawyers import lawyers_bp
    from routes.documents import documents_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(advisory_bp, url_prefix="/api/advisory")
    app.register_blueprint(lawyers_bp, url_prefix="/api/lawyers")
    app.register_blueprint(documents_bp, url_prefix="/api/documents")

    # ── Health Check ────────────────────────────────────────────
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "adaalat-backend"}), 200

    # ── Error Handlers ──────────────────────────────────────────
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request", "message": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


# ── Entry Point ─────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
