from flask import jsonify
from app.modules.users.service import UserService
from app.core.security.password import verify_password, hash_password


class UserController:

    @staticmethod
    def create(data, db):

        if UserService.get_by_email(db, data.get("email")):
            return jsonify({"message": "Email already exists"}), 400

        if UserService.get_by_username(db, data.get("username")):
            return jsonify({"message": "Username already exists"}), 400

        hashed_password = hash_password(data.get("password"))

        user_data = {
            "username": data.get("username"),
            "email": data.get("email"),
            "password_hash": hashed_password,
            "phone": data.get("phone"),
            "address": data.get("address"),
            "role_id": data.get("role_id"),
        }

        user = UserService.create_user(db, user_data)

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role_id": user.role_id,
            "created_at": user.created_at.isoformat()
        }), 201

    @staticmethod
    def get_all(db):

        users = UserService.get_users(db)

        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "phone": u.phone,
                "role_id": u.role_id,
                "created_at": u.created_at.isoformat()
            }
            for u in users
        ]), 200

    @staticmethod
    def get_one(user_id, db):

        user = UserService.get_user_by_id(db, user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role_id": user.role_id,
            "created_at": user.created_at.isoformat()
        }), 200

    @staticmethod
    def update(user_id, data, db):

        user = UserService.get_user_by_id(db, user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        if "password" in data:
            data["password_hash"] = hash_password(data["password"])
            del data["password"]

        updated_user = UserService.update_user(db, user, data)

        return jsonify({
            "id": updated_user.id,
            "username": updated_user.username,
            "email": updated_user.email,
            "updated_at": updated_user.updated_at.isoformat()
        }), 200

    @staticmethod
    def delete(user_id, db):

        user = UserService.get_user_by_id(db, user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        UserService.delete_user(db, user)

        return jsonify({"message": "User deleted"}), 200