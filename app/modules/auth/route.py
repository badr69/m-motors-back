from flask import Blueprint, request
from app.modules.auth.controller import AuthController
from app.core.security.jwt_middleware import jwt_required

auth_bp = Blueprint("auth", __name__)

# =====================
# REGISTER
# =====================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    return AuthController.register(data)

# =====================
# LOGIN
# =====================
@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login()

# =====================
# REFRESH
# =====================
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    auth_header = request.headers.get("Authorization")
    return AuthController.refresh(auth_header)

# =====================
# CURRENT USER
# =====================
@auth_bp.route("/currentUser", methods=["GET"])
@jwt_required
def current_user():
    return AuthController.current_user()

# =====================
# LOGOUT
# =====================
@auth_bp.route("/logout", methods=["POST"])
@jwt_required
def logout():
    return AuthController.logout()