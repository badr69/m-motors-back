from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from app.core.config import Config
from app.core.db import Base, engine


def create_app():

    # LOAD ENV
    load_dotenv()

    # APP INIT
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS
    # CORS(
    #     app,
    #     resources={r"/api/v1/*": {"origins": "*"}},
    #     supports_credentials=True
    # )
    CORS(
        app,
        resources={r"/api/v1/*": {
            "origins": ["http://127.0.0.1:5500",
                        "http://84.46.241.76:8080"
            ]
        }},
        supports_credentials=True
    )

    # DB INIT
    Base.metadata.create_all(bind=engine)

    # ROUTES
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    # ERRORS
    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Route not found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {"message": "Internal server error"}, 500

    return app