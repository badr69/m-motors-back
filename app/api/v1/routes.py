from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__)

@api_v1.route("/health")
def health():
    return {"status": "ok"}