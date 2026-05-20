# roles/route.py
from flask import Blueprint, request
from app.modules.roles.controller import RoleController
from app.core.security.decorators import login_required, admin_required

role_bp = Blueprint("roles", __name__)


# =====================
# CREATE + GET ALL
# =====================
@role_bp.route("", methods=["GET", "POST"])
@login_required
@admin_required
def roles():

    if request.method == "GET":
        return RoleController.get_all()

    return RoleController.create(request.get_json())


# =====================
# GET ONE
# =====================
@role_bp.route("/<int:role_id>", methods=["GET"])
@login_required
def get_role(role_id):
    return RoleController.get_one(role_id)


# =====================
# UPDATE
# =====================
@role_bp.route("/<int:role_id>", methods=["PUT"])
@login_required
@admin_required
def update_role(role_id):
    return RoleController.update(role_id, request.get_json())


# =====================
# DELETE
# =====================
@role_bp.route("/<int:role_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_role(role_id):
    return RoleController.delete(role_id)