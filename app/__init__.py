from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from app.core.config import Config
from app.core.db import Base, engine


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
    # CORS (IMPORTANT FRONTEND JS)
    # =====================
    CORS(
        app,
        resources={r"/api/v1/*": {
            "origins": [
                "http://84.46.241.76:8080",
                "http://127.0.0.1:5500"
            ]
        }},
        supports_credentials=True
    )

    # =====================
    # DATABASE INIT (DEV ONLY)
    # =====================
    # Base.metadata.create_all(bind=engine)

    # =====================
    # BLUEPRINTS
    # =====================
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    # =====================
    # ROOT ROUTE (AJOUTÉ ICI)
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