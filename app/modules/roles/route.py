from flask import Blueprint, request
from app.modules.roles.controller import RoleController
from app.core.security.jwt_middleware import jwt_required
from app.core.security.decorators import require_role

role_bp = Blueprint("roles", __name__)


# =====================
# GET ALL (ADMIN ONLY)
# =====================
@role_bp.route("", methods=["GET"])
@jwt_required
@require_role("ADMIN")
def get_roles():
    return RoleController.get_all()


# =====================
# CREATE (ADMIN ONLY)
# =====================
@role_bp.route("", methods=["POST"])
@jwt_required
@require_role("ADMIN")
def create_role():
    return RoleController.create_role()
# @role_bp.route("", methods=["POST"])
# @jwt_required
# @require_role("ADMIN")
# def create_role():
#     data = request.get_json() or {}
#     return RoleController.create_role(data)


# =====================
# GET ONE (ADMIN ONLY)
# =====================
@role_bp.route("/<int:role_id>", methods=["GET"])
@jwt_required
@require_role("ADMIN")
def get_role(role_id):
    return RoleController.get_one(role_id)


# =====================
# UPDATE (ADMIN ONLY)
# =====================
@role_bp.route("/<int:role_id>", methods=["PUT"])
@jwt_required
@require_role("ADMIN")
def update_role(role_id):
    return RoleController.update(role_id)


# =====================
# DELETE (ADMIN ONLY)
# =====================
@role_bp.route("/<int:role_id>", methods=["DELETE"])
@jwt_required
@require_role("ADMIN")
def delete_role(role_id):
    return RoleController.delete(role_id)