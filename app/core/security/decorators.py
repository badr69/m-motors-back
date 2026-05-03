from functools import wraps
from flask import request, jsonify
from app.core.security.jwt import decode_token


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token missing"}), 401

        try:
            parts = auth_header.split(" ")

            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"message": "Invalid token format"}), 401

            token = parts[1]
            payload = decode_token(token)

            request.user = payload

        except Exception:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = getattr(request, "user", None)

        if not user:
            return jsonify({"message": "Unauthorized"}), 401

        if user.get("role") != "ADMIN":
            return jsonify({"message": "Forbidden (admin only)"}), 403

        return f(*args, **kwargs)

    return decorated