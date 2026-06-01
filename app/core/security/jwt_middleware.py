from functools import wraps
from flask import request, jsonify
from app.core.security.jwt import decode_token


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        print("[AUTH HEADER]", auth_header)

        if not auth_header:
            return jsonify({"message": "Token missing"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid auth format"}), 401

        token = parts[1]

        try:
            payload = decode_token(token)
            print("[JWT PAYLOAD]", payload)

            if not payload:
                return jsonify({"message": "Invalid token"}), 401

            request.current_user = {
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "role": (payload.get("role") or "").lower()
            }

        except Exception as e:
            print("[JWT ERROR]", str(e))
            return jsonify({"message": "Token invalid or expired"}), 401

        return f(*args, **kwargs)

    return decorated