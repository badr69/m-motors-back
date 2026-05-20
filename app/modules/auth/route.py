from flask import Blueprint, request
from app.modules.auth.controller import AuthController
from app.core.security.decorators import login_required

auth_bp = Blueprint("auth", __name__)


# =====================
# LOGIN
# =====================
@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login(request.get_json())


# =====================
# REFRESH
# =====================
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    return AuthController.refresh(
        request.headers.get("Authorization")
    )


# =====================
# LOGOUT
# =====================
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    return AuthController.logout()


# =====================
# CURRENT USER
# =====================
@auth_bp.route("/currentUser", methods=["GET"])
@login_required
def current_user():
    return AuthController.current_user(
        request.headers.get("Authorization")
    )