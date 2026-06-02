from flask import Blueprint, request, g, jsonify
from app.modules.users.controller import UserController
from app.core.security.decorators import jwt_required, admin_required

users_bp = Blueprint("users", __name__)

# =====================
# GET ALL USERS (ADMIN ONLY)
# =====================
@users_bp.route("", methods=["GET"])
@jwt_required
@admin_required
def get_users():
    return UserController.get_users()


# =====================
# CREATE USER (ADMIN ONLY)
# =====================
@users_bp.route("", methods=["POST"])
@admin_required
def create_user():
    data = request.get_json() or {}
    return UserController.create_user(data)


# =====================
# GET USER BY ID
# =====================
@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required
def get_user(user_id):
    return UserController.get_user(user_id)


# =====================
# UPDATE USER
# =====================
@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required
def update_user(user_id):
    data = request.get_json() or {}
    return UserController.update_user(user_id, data, g.current_user)


# =====================
# DELETE USER
# =====================
# =====================
# DELETE USER
# =====================
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required
def delete_user(user_id):
    return UserController.delete_user(
        user_id,
        g.current_user
    )

# =====================
# CURRENT USER
# =====================
@users_bp.route("/me", methods=["GET"])
@jwt_required
def get_me():
    return jsonify(g.current_user)