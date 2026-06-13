from flask import Blueprint
from app.modules.users.controller import UserController
from app.core.security.jwt_middleware import jwt_required
from app.core.security.decorators import require_role

user_bp = Blueprint("users", __name__)

# =====================
# ADMIN ONLY
# =====================

@user_bp.route("", methods=["GET"])
@jwt_required
@require_role("ADMIN")
def get_users():
    return UserController.get_users()


@user_bp.route("", methods=["POST"])
@jwt_required
@require_role("ADMIN")
def create_user():
    return UserController.create_user()


# =====================
# GET USER BY ID (ADMIN + CLIENT OWN CHECK IN SERVICE)
# =====================
@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required
@require_role("ADMIN", "CLIENT")
def get_user_by_id(user_id):
    return UserController.get_user_by_id(user_id)


@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required
@require_role("ADMIN")
def update_user(user_id):
    return UserController.update_user(user_id)


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required
@require_role("ADMIN")
def delete_user(user_id):
    return UserController.delete_user(user_id)


# =====================
# SELF SERVICE (ME)
# =====================

@user_bp.route("/me", methods=["GET"])
@jwt_required
def get_me():
    return UserController.get_me()


@user_bp.route("/me", methods=["PUT"])
@jwt_required
def update_me():
    return UserController.update_me()


@user_bp.route("/me", methods=["DELETE"])
@jwt_required
def delete_me():
    return UserController.delete_me()

