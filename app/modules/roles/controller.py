# roles/controller.py
from flask import jsonify
from app.modules.roles.service import RoleService


class RoleController:

    @staticmethod
    def create(data, db):

        role, error = RoleService.create_role(db, data.get("name"))

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "id": role.id,
            "name": role.name,
            "created_at": role.created_at.isoformat(),
            "updated_at": role.updated_at.isoformat()
        }), 201

    @staticmethod
    def get_all(db):

        roles = RoleService.get_roles(db)

        return jsonify([
            {
                "id": r.id,
                "name": r.name,
                "created_at": r.created_at.isoformat(),
                "updated_at": r.updated_at.isoformat()
            }
            for r in roles
        ]), 200

    @staticmethod
    def get_one(role_id, db):

        role = RoleService.get_role_by_id(db, role_id)

        if not role:
            return jsonify({"message": "Role not found"}), 404

        return jsonify({
            "id": role.id,
            "name": role.name,
            "created_at": role.created_at.isoformat(),
            "updated_at": role.updated_at.isoformat()
        }), 200

    @staticmethod
    def update(role_id, data, db):

        role = RoleService.get_role_by_id(db, role_id)

        if not role:
            return jsonify({"message": "Role not found"}), 404

        if role.name == "ADMIN":
            return jsonify({"message": "ADMIN role cannot be modified"}), 403

        role, error = RoleService.update_role(db, role, data.get("name"))

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "id": role.id,
            "name": role.name,
            "updated_at": role.updated_at.isoformat()
        }), 200

    @staticmethod
    def delete(role_id, db):

        role = RoleService.get_role_by_id(db, role_id)

        if not role:
            return jsonify({"message": "Role not found"}), 404

        if role.name == "ADMIN":
            return jsonify({"message": "ADMIN role cannot be deleted"}), 403

        RoleService.delete_role(db, role)

        return jsonify({"message": "Role deleted"}), 200