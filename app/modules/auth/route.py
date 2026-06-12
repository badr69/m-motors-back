from flask import Blueprint
from app.modules.auth.controller import AuthController
from app.core.security.jwt_middleware import jwt_required

auth_bp = Blueprint("auth", __name__)

# =====================
# PUBLIC ROUTES
# =====================

@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login()

@auth_bp.route("/register", methods=["POST"])
def register():
    return AuthController.register()


# =====================
# PROTECTED ROUTES
# =====================

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required
def refresh():
    return AuthController.refresh()

@auth_bp.route("/logout", methods=["POST"])
@jwt_required
def logout():
    return AuthController.logout()

@auth_bp.route("/me", methods=["GET"])
@jwt_required
def me():
    return AuthController.current_user()