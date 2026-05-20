from flask import Blueprint, request
from app.modules.users.controller import UserController
from app.core.security.decorators import login_required, admin_required

users_bp = Blueprint("users", __name__)


# =====================
# CREATE USER (ADMIN ONLY)
# =====================
@users_bp.route("", methods=["POST"])
@login_required
@admin_required
def create_user():
    return UserController.create(request.get_json())


# =====================
# GET ALL USERS (ADMIN ONLY)
# =====================
@users_bp.route("", methods=["GET"])
@login_required
@admin_required
def get_users():
    return UserController.get_all()


# =====================
# GET ONE USER
# =====================
@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):
    return UserController.get_one(user_id)


# =====================
# UPDATE USER
# =====================
@users_bp.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    return UserController.update(user_id, request.get_json())


# =====================
# DELETE USER
# =====================
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_user(user_id):
    return UserController.delete(user_id)