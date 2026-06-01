from flask import request, jsonify
from app.modules.users.service import UserService
from app.core.security.jwt_middleware import jwt_required


class UserController:

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    @jwt_required
    def create_user():

        data = request.get_json() or {}

        result, error = UserService.create_user(data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "message": "User created successfully",
            "user": {
                "id": result.id,
                "username": result.username,
                "email": result.email,
                "role": result.role.name if result.role else None
            }
        }), 201

    # =====================
    # GET ALL USERS
    # =====================
    @staticmethod
    @jwt_required
    def get_users():

        users = UserService.get_users()

        data = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "phone": u.phone,
                "address": u.address,
                "role": u.role.name if u.role else None
            }
            for u in users
        ]

        return jsonify(data), 200

    # =====================
    # GET USER BY ID
    # =====================
    @staticmethod
    @jwt_required
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
            "role": user.role.name if user.role else None,
            "role_id": user.role_id
        }), 200

    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    @jwt_required
    def update_user(user_id):

        data = request.get_json() or {}
        current_user = request.current_user

        result, error = UserService.update_user(user_id, data, current_user)

        if error:
            return jsonify({"message": error}), 403

        return jsonify(result), 200

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    @jwt_required
    def delete_user(user_id):

        current_user = request.current_user

        success, error = UserService.delete_user(user_id, current_user)

        if error:
            return jsonify({"message": error}), 403

        return jsonify({"message": "User deleted successfully"}), 200

    # =====================
    # ME
    # =====================
    @staticmethod
    @jwt_required
    def get_me():

        user_id = request.current_user["user_id"]

        result, error = UserService.get_me(user_id)

        if error:
            return jsonify({"message": error}), 404

        return jsonify(result), 200

    # =====================
    # UPDATE ME
    # =====================
    @staticmethod
    @jwt_required
    def update_me():

        user_id = request.current_user["user_id"]
        data = request.get_json() or {}

        result, error = UserService.update_me(user_id, data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify(result), 200

    # =====================
    # DELETE ME
    # =====================
    @staticmethod
    @jwt_required
    def delete_me():

        user_id = request.current_user["user_id"]

        success, error = UserService.delete_me(user_id)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({"message": "Account deleted successfully"}), 200

