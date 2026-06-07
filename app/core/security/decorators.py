from functools import wraps
from flask import request, jsonify


def require_role(*allowed_roles):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            # =====================
            # GET CURRENT USER FROM REQUEST (JWT)
            # =====================
            current_user = getattr(request, "current_user", None)

            if not current_user:
                return jsonify({
                    "message": "Unauthorized"
                }), 401

            user_role = (current_user.get("role") or "").upper()

            # =====================
            # NORMALIZE ROLES
            # =====================
            normalized_allowed_roles = [
                role.upper() for role in allowed_roles
            ]

            # =====================
            # ACCESS CHECK
            # =====================
            if user_role not in normalized_allowed_roles:
                return jsonify({
                    "message": "Forbidden"
                }), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator




