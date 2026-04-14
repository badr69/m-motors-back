from flask import Flask
from dotenv import load_dotenv

from app.core.config import Config


def create_app():

    # load env
    load_dotenv()

    app = Flask(__name__)

    # config
    app.config.from_object(Config)

    # IMPORT LOCAL (IMPORTANT)
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    return app