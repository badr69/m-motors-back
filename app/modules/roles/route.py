from flask import Blueprint, request
from app.modules.roles.controller import RoleController
from app.core.security.decorators import login_required, admin_required

role_bp = Blueprint("roles", __name__)


# =====================
# GET ALL
# =====================
@role_bp.route("", methods=["GET"])
@login_required
@admin_required
def get_roles():
    return RoleController.get_all()


# =====================
# CREATE
# =====================
@role_bp.route("", methods=["POST"])
@login_required
def create_role():
    data = request.get_json() or {}
    return RoleController.create(data)


# =====================
# GET ONE
# =====================
@role_bp.route("/<int:role_id>", methods=["GET"])
@login_required
@admin_required
def get_role(role_id):
    return RoleController.get_one(role_id)


# =====================
# UPDATE
# =====================
@role_bp.route("/<int:role_id>", methods=["PUT"])
@login_required
@admin_required
def update_role(role_id):
    data = request.get_json() or {}
    return RoleController.update(role_id, data)


# =====================
# DELETE
# =====================
@role_bp.route("/<int:role_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_role(role_id):
    return RoleController.delete(role_id)
