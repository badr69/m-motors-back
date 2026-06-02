from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from app.core.config import Config
from app.core.db import Base, engine, SessionLocal

from app.modules.roles.seed import seed_roles


def create_app():

    # =====================
    # LOAD ENV
    # =====================
    load_dotenv()

    # =====================
    # INIT APP
    # =====================
    app = Flask(__name__)
    app.config.from_object(Config)

    # =====================
    # CORS
    # =====================
    CORS(
        app,
        resources={r"/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500"
            ]
        }},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response


    # =====================
    # DATABASE INIT (DEV ONLY)
    # =====================
    # Base.metadata.create_all(bind=engine)  # ❌ laissé OFF (normal)

    # =====================
    # SEED ROLES (IMPORTANT)
    # =====================
    try:
        db = SessionLocal()
        seed_roles(db)
        db.close()
        print("[SEED] Roles OK")
    except Exception as e:
        print(f"[SEED ERROR] {e}")

    # =====================
    # BLUEPRINTS
    # =====================
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    # =====================
    # ROOT ROUTE
    # =====================
    @app.route("/")
    def home():
        return {
            "message": "M-Motors API",
            "status": "running",
            "version": "v1"
        }

    # =====================
    # ERROR HANDLERS
    # =====================
    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Route not found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {"message": "Internal server error"}, 500

    return app