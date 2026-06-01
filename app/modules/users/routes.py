from flask import Blueprint, request
from app.modules.users.controller import UserController
from app.core.security.decorators import login_required, admin_required

users_bp = Blueprint("users", __name__)

@users_bp.route("", methods=["GET"])
@login_required
@admin_required
def get_users():
    return UserController.get_users()


@users_bp.route("", methods=["POST"])
@login_required
@admin_required
def create_user():
    return UserController.create_user()


@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):
    return UserController.get_user(user_id)


@users_bp.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    return UserController.update_user(user_id)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    return UserController.delete_user(user_id)

@users_bp.route("/me", methods=["GET"])
@login_required
def get_me():
    return UserController.get_me()