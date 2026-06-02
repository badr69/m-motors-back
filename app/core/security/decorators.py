from functools import wraps
from flask import g, jsonify
from app.core.security.jwt_middleware import jwt_required


def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        # =====================
        # DEBUG MINIMAL
        # =====================
        user = getattr(g, "current_user", None)

        print("[ADMIN DEBUG] current_user =", user)

        if not user:
            print("[ADMIN DEBUG] NO USER IN CONTEXT")
            return jsonify({"message": "Unauthorized"}), 401

        role = (user.get("role") or "").upper().strip()

        print("[ADMIN DEBUG] role =", role)

        # =====================
        # CHECK ADMIN ROLE
        # =====================
        if role != "ADMIN":
            print("[ADMIN DEBUG] FORBIDDEN ACCESS")
            return jsonify({"message": "Forbidden (admin only)"}), 403

        print("[ADMIN DEBUG] ACCESS GRANTED")

        return f(*args, **kwargs)

    # IMPORTANT: JWT FIRST, THEN ADMIN CHECK
    return jwt_required(decorated)