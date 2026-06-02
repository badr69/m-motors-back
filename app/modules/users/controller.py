from flask import jsonify
from app.modules.users.service import UserService


class UserController:

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    def create_user(data):

        result, error = UserService.create_user(data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "message": "User created successfully",
            "user": {
                "id": result.id,
                "username": result.username,
                "email": result.email,
                "phone": result.phone,
                "address": result.address,
                "role": result.role.name if result.role else None
            }
        }), 201

    # =====================
    # GET ALL USERS
    # =====================
    @staticmethod
    def get_users():

        users, error = UserService.get_users()

        if error:
            return jsonify({"message": error}), 500

        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "phone": u.phone,
                "address": u.address,
                "role": u.role.name if u.role else None
            }
            for u in users
        ]), 200

    # =====================
    # GET USER BY ID
    # =====================
    @staticmethod
    def get_user(user_id):

        user, error = UserService.get_user_by_id(user_id)

        if error:
            return jsonify({"message": error}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role": user.role.name if user.role else None
        }), 200

    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update_user(user_id, data, current_user):

        result, error = UserService.update_user(user_id, data, current_user)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "message": "User updated successfully",
            "user": {
                "id": result.id,
                "username": result.username,
                "email": result.email,
                "phone": result.phone,
                "address": result.address,
                "role": result.role.name if result.role else None
            }
        }), 200

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete_user(user_id, current_user):

        success, error = UserService.delete_user(user_id, current_user)

        if not success:
            return jsonify({
                "message": error
            }), 400

        return jsonify({
            "message": "User deleted successfully"
        }), 200