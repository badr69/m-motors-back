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

        return jsonify(role), 201


    # =====================
    # GET ALL
    # =====================
    @staticmethod
    def get_all():

        roles = RoleService.get_roles()

        return jsonify(roles), 200


    # =====================
    # GET ONE
    # =====================
    @staticmethod
    def get_one(role_id):

        role, error = RoleService.get_role_by_id(role_id)

        if error:
            return jsonify({"message": error}), 404

        return jsonify(role), 200


    # =====================
    # UPDATE
    # =====================
    @staticmethod
    def update(role_id, data):

        role, error = RoleService.update_role(role_id, data.get("name"))

        if error:
            return jsonify({"message": error}), 400

        return jsonify(role), 200


    # =====================
    # DELETE
    # =====================
    @staticmethod
    def delete(role_id):

        success, error = RoleService.delete_role(role_id)

        if not success:
            return jsonify({"message": error}), 403

        return jsonify({"message": "Role deleted"}), 200




