from flask import Blueprint, request
from app.modules.roles.controller import RoleController
from app.core.security.decorators import jwt_required, admin_required


role_bp = Blueprint("roles", __name__)


# =====================
# GET ALL ROLES (ADMIN ONLY)
# =====================
@role_bp.route("", methods=["GET"])
@jwt_required
@admin_required
def get_roles():
    return RoleController.get_all()

# =====================
# CREATE ROLE (ADMIN ONLY)
# =====================
@role_bp.route("", methods=["POST"])
@jwt_required
@admin_required
def create_role():
    data = request.get_json() or {}
    return RoleController.create(data)

# =====================
# GET ONE ROLE (ADMIN ONLY)
# =====================
@role_bp.route("/<int:role_id>", methods=["GET"])
@jwt_required
@admin_required
def get_role(role_id):
    return RoleController.get_one(role_id)

# =====================
# UPDATE ROLE (ADMIN ONLY)
# =====================
@role_bp.route("/<int:role_id>", methods=["PUT"])
@jwt_required
@admin_required
def update_role(role_id):
    data = request.get_json() or {}
    return RoleController.update(role_id, data)

# =====================
# DELETE ROLE (ADMIN ONLY)
# =====================
@role_bp.route("/<int:role_id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_role(role_id):
    return RoleController.delete(role_id)