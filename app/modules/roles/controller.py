# roles/controller.py
from flask import jsonify
from app.modules.roles.service import RoleService


class RoleController:

    # =====================
    # CREATE
    # =====================
    @staticmethod
    def create(data):

        role, error = RoleService.create_role(data.get("name"))

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "id": role.id,
            "name": role.name,
            "created_at": role.created_at.isoformat(),
            "updated_at": role.updated_at.isoformat()
        }), 201

    # =====================
    # GET ALL
    # =====================
    @staticmethod
    def get_all():

        roles = RoleService.get_roles()

        return jsonify([
            {
                "id": r.id,
                "name": r.name,
                "created_at": r.created_at.isoformat(),
                "updated_at": r.updated_at.isoformat()
            }
            for r in roles
        ]), 200

    # =====================
    # GET ONE
    # =====================
    @staticmethod
    def get_one(role_id):

        role = RoleService.get_role_by_id(role_id)

        if not role:
            return jsonify({"message": "Role not found"}), 404

        return jsonify({
            "id": role.id,
            "name": role.name,
            "created_at": role.created_at.isoformat(),
            "updated_at": role.updated_at.isoformat()
        }), 200

    # =====================
    # UPDATE
    # =====================
    @staticmethod
    def update(role_id, data):

        role = RoleService.get_role_by_id(role_id)

        if not role:
            return jsonify({"message": "Role not found"}), 404

        if role.name == "ADMIN":
            return jsonify({"message": "ADMIN role cannot be modified"}), 403

        role, error = RoleService.update_role(role_id, data.get("name"))

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "id": role.id,
            "name": role.name,
            "updated_at": role.updated_at.isoformat()
        }), 200

    # =====================
    # DELETE
    # =====================
    @staticmethod
    def delete(role_id):

        role = RoleService.get_role_by_id(role_id)

        if not role:
            return jsonify({"message": "Role not found"}), 404

        if role.name == "ADMIN":
            return jsonify({"message": "ADMIN role cannot be deleted"}), 403

        error = RoleService.delete_role(role_id)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({"message": "Role deleted"}), 200