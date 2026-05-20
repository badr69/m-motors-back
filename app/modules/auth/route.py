from flask import Blueprint, request
from app.modules.auth.controller import AuthController
from app.core.security.decorators import login_required
from app.core.security.jwt_middleware import jwt_required


auth_bp = Blueprint("auth", __name__)

# =====================
# LOGIN
# =====================
@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login()

# =====================
# REGISTER
# =====================
@auth_bp.route("/register", methods=["POST"])
def register():
    return AuthController.register()


# =====================
# REFRESH TOKEN
# =====================
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    return AuthController.refresh()

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
@jwt_required
def current_user():
    return AuthController.current_user()
