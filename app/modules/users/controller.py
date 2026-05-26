from flask import jsonify, request
from app.modules.users.service import UserService


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
    def update(user_id, data, current_user):

        user, error = UserService.update_user(user_id, data, current_user)

        if error:
            return jsonify({"message": error}), 403

        return jsonify(user), 200

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete(user_id, current_user):

        success, error = UserService.delete_user(user_id, current_user)

        if not success:
            return jsonify({"message": error}), 403

        return jsonify({"message": "User deleted"}), 200

    # =====================
    # GET ME
    # =====================
    @staticmethod
    def get_me(current_user):

        data, error = UserService.get_me(current_user)

        return jsonify(data), 200

    # =====================
    # UPDATE ME
    # =====================
    @staticmethod
    def update_me(current_user, data):

        user, error = UserService.update_me(current_user, data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify(user), 200

    # =====================
    # DELETE ME
    # =====================
    @staticmethod
    def delete_me(current_user, db):

        success, error = UserService.delete_me(current_user, db)

        if not success:
            return jsonify({"message": error}), 400

        return jsonify({"message": "Account deleted"}), 200
