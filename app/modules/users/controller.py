from flask import jsonify
from app.modules.users.service import UserService
from app.core.security.password import hash_password


class UserController:

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    def create(data):

        user, error = UserService.create_user(data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role_id": user.role_id
        }), 201


    # =====================
    # GET ALL USERS
    # =====================
    @staticmethod
    def get_all():

        users = UserService.get_users()
        print("FIRST USER:", users[0].phone, users[0].address)

        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "phone": u.phone,
                "address": u.address,
                "role_id": u.role_id
            }
            for u in users
        ]), 200


    # =====================
    # GET ONE USER
    # =====================
    @staticmethod
    def get_one(user_id):

        user, error = UserService.get_user_by_id(user_id)

        if error:
            return jsonify({"message": error}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role_id": user.role_id
        }), 200


    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update(user_id, data):

        user, error = UserService.update_user(user_id, data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({
            "id": user.id,
            "username": user.username
        }), 200


    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete(user_id):

        ok, error = UserService.delete_user(user_id)

        if error:
            return jsonify({"message": error}), 400

        return jsonify({"message": "User deleted"}), 200
