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

            if payload.get("type") != "access":
                return jsonify({"message": "Invalid token type"}), 401

            # 👇 IMPORTANT : injection user_id
            request.user_id = payload.get("user_id")

        except Exception:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated