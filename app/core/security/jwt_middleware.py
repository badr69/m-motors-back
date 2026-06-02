from functools import wraps
from flask import request, jsonify, g
from app.core.security.jwt import decode_token


def jwt_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        print("\n[JWT] middleware hit")

        auth_header = request.headers.get("Authorization")

        print("[JWT DEBUG] Authorization header =", auth_header)

        if not auth_header:
            print("[JWT ERROR] missing header")
            return jsonify({"message": "Token missing"}), 401

        parts = auth_header.split(" ")

        print("[JWT DEBUG] parts =", parts)

        if len(parts) != 2:
            print("[JWT ERROR] bad format")
            return jsonify({"message": "Invalid auth format"}), 401

        if parts[0].lower() != "bearer":
            print("[JWT ERROR] invalid scheme =", parts[0])
            return jsonify({"message": "Invalid auth format"}), 401

        token = parts[1]

        print("[JWT DEBUG] token =", token[:25], "...")

        payload = decode_token(token)

        if not payload:
            print("[JWT ERROR] invalid/expired token")
            return jsonify({"message": "Invalid token"}), 401

        g.current_user = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "role": (payload.get("role") or "USER").upper().strip()
        }

        print("[JWT DEBUG] user =", g.current_user)

        print("[JWT] OK")

        return f(*args, **kwargs)

    return decorated