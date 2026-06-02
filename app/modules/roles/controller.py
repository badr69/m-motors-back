from flask import jsonify
from app.modules.roles.service import RoleService


class RoleController:

    # =====================
    # CREATE ROLE
    # =====================
    @staticmethod
    def create(data):

        role, error = RoleService.create_role(data.get("name"))

        if error:
            return jsonify({"message": error}), 400

        return jsonify(role), 201

    # =====================
    # GET ALL ROLES
    # =====================
    @staticmethod
    def get_all():

        roles, error = RoleService.get_roles()

        if error:
            return jsonify({"message": error}), 500

        return jsonify(roles), 200

    # =====================
    # GET ROLE BY ID
    # =====================
    @staticmethod
    def get_one(role_id):

        role, error = RoleService.get_role_by_id(role_id)

        if error:
            return jsonify({"message": error}), 404

        return jsonify(role), 200

    # =====================
    # UPDATE ROLE
    # =====================
    @staticmethod
    def update(role_id, data):

        role, error = RoleService.update_role(role_id, data.get("name"))

        if error:
            return jsonify({"message": error}), 400

        return jsonify(role), 200

    # =====================
    # DELETE ROLE
    # =====================
    @staticmethod
    def delete(role_id):

        success, error = RoleService.delete_role(role_id)

        if not success:
            return jsonify({"message": error}), 403

        return jsonify({"message": "Role deleted"}), 200
