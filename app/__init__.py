import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from app.core.config import Config
from app.core.db import Base, engine, SessionLocal
from app.modules.roles.seed import seed_roles
from flask import send_from_directory

def create_app():

    # =====================
    # LOAD ENV
    # =====================
    load_dotenv()

    # =====================
    # SENTRY CONFIG
    # =====================
    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                FlaskIntegration(),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=1.0,
            environment=os.getenv('SENTRY_ENVIRONMENT', 'development'),
            release="v1.0.0",
        )
        print("✅ Sentry initialisé")
    else:
        print("⚠️ Sentry DSN non configuré")

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
        resources={r"/api/v1/*": {"origins": "*"}},
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
    # Base.metadata.create_all(bind=engine)  # OFF volontaire

    # =====================
    # SEED ROLES (SAFE CONTEXT)
    # =====================
    with app.app_context():
        db = SessionLocal()
        try:
            seed_roles(db)
            print("[SEED] Roles OK")
        except Exception as e:
            print(f"[SEED ERROR] {e}")
            sentry_sdk.capture_exception(e)  # ← Envoyer l'erreur à Sentry
        finally:
            db.close()

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
        sentry_sdk.capture_exception(error)  # ← Envoyer à Sentry
        return {"message": "Route not found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        sentry_sdk.capture_exception(error)  # ← Envoyer à Sentry
        return {"message": "Internal server error"}, 500

    # =====================
    # ROUTE DE TEST SENTRY
    # =====================
    @app.route("/test-sentry")
    def test_sentry():
        try:
            1 / 0
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return {"error": str(e), "message": "Erreur envoyée à Sentry"}, 500


    @app.route("/uploads/vehicles/<path:filename>")
    def serve_vehicle_image(filename):

        upload_folder = os.path.join(
            app.root_path,
            "..",
            "uploads",
            "vehicles"
        )

        upload_folder = os.path.abspath(upload_folder)

        print("UPLOAD FOLDER =", upload_folder)
        print("FILENAME =", filename)

        return send_from_directory(
            upload_folder,
            filename
        )

    return app