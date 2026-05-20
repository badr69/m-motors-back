from functools import wraps
from flask import request, jsonify
from app.core.security.jwt import decode_token


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Missing token"}), 401

        try:
            token = auth_header.split(" ")[1]
            payload = decode_token(token)

            request.user_id = payload.get("user_id")

        except Exception as e:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated