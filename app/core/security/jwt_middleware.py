from functools import wraps
from flask import request, jsonify
from app.core.security.jwt import decode_token


def jwt_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        # =====================
        # GET AUTH HEADER
        # =====================
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token missing"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid auth format"}), 401

        token = parts[1]

        # =====================
        # DECODE TOKEN
        # =====================
        payload = decode_token(token)

        if not payload:
            return jsonify({"message": "Invalid or expired token"}), 401

        # =====================
        # BUILD USER CONTEXT (STRICT)
        # =====================
        request.current_user = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "role": (payload.get("role") or "").upper()
        }

        return f(*args, **kwargs)

    return decorated