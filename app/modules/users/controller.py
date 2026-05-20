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

        return jsonify([
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
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








# # from flask import jsonify
# # from app.modules.users.service import UserService
# # from app.core.security.password import verify_password, hash_password
# #
# #
# # class UserController:
# #
# #     @staticmethod
# #     def create(data, db):
# #
# #         if UserService.get_by_email(db, data.get("emailfrom flask import jsonify
# from app.modules.users.service import UserService
# from app.core.security.password import hash_password
#
#
# class UserController:
#
#     # =====================
#     # CREATE USER
#     # =====================
#     @staticmethod
#     def create(data):
#
#         user, error = UserService.create_user(data)
#
#         if error:
#             return jsonify({"message": error}), 400
#
#         return jsonify({
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "role_id": user.role_id
#         }), 201
#
#
#     # =====================
#     # GET ALL USERS
#     # =====================
#     @staticmethod
#     def get_all():
#
#         users = UserService.get_users()
#
#         return jsonify([
#             {
#                 "id": u.id,
#                 "username": u.username,
#                 "email": u.email,
#                 "role_id": u.role_id
#             }
#             for u in users
#         ]), 200
#
#
#     # =====================
#     # GET ONE USER
#     # =====================
#     @staticmethod
#     def get_one(user_id):
#
#         user, error = UserService.get_user_by_id(user_id)
#
#         if error:
#             return jsonify({"message": error}), 404
#
#         return jsonify({
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "role_id": user.role_id
#         }), 200
#
#
#     # =====================
#     # UPDATE USER
#     # =====================
#     @staticmethod
#     def update(user_id, data):
#
#         user, error = UserService.update_user(user_id, data)
#
#         if error:
#             return jsonify({"message": error}), 400
#
#         return jsonify({
#             "id": user.id,
#             "username": user.username
#         }), 200
#
#
#     # =====================
#     # DELETE USER
#     # =====================
#     @staticmethod
#     def delete(user_id):
#
#         ok, error = UserService.delete_user(user_id)
#
#         if error:
#             return jsonify({"message": error}), 400
#
#         return jsonify({"message": "User deleted"}), 200")):
# #             return jsonify({"message": "Email already exists"}), 400
# #
# #         if UserService.get_by_username(db, data.get("username")):
# #             return jsonify({"message": "Username already exists"}), 400
# #
# #         hashed_password = hash_password(data.get("password"))
# #
# #         user_data = {
# #             "username": data.get("username"),
# #             "email": data.get("email"),
# #             "password_hash": hashed_password,
# #             "phone": data.get("phone"),
# #             "address": data.get("address"),
# #             "role_id": data.get("role_id"),
# #         }
# #
# #         # ✅ FIX ICI
# #         user, error = UserService.create_user(db, user_data)
# #
# #         if error:
# #             return jsonify({"message": error}), 400
# #
# #         return jsonify({
# #             "id": user.id,
# #             "username": user.username,
# #             "email": user.email,
# #             "phone": user.phone,
# #             "address": user.address,
# #             "role_id": user.role_id,
# #             "created_at": user.created_at.isoformat()
# #         }), 201
# #
# #     @staticmethod
# #     def get_all(db):
# #
# #         users = UserService.get_users(db)
# #
# #         return jsonify([
# #             {
# #                 "id": u.id,
# #                 "username": u.username,
# #                 "email": u.email,
# #                 "phone": u.phone,
# #                 "address": u.address,
# #                 "role_id": u.role_id,
# #
# #                 # ✅ AJOUT IMPORTANT
# #                 "role": {
# #                     "id": u.role.id,
# #                     "name": u.role.name
# #                 } if u.role else None,
# #
# #                 "created_at": u.created_at.isoformat()
# #             }
# #             for u in users
# #         ]), 200
# #
# #     @staticmethod
# #     def get_one(user_id, db):
# #
# #         user = UserService.get_user_by_id(db, user_id)
# #
# #         if not user:
# #             return jsonify({"message": "User not found"}), 404
# #
# #         return jsonify({
# #             "id": user.id,
# #             "username": user.username,
# #             "email": user.email,
# #             "phone": user.phone,
# #             "address": user.address,
# #             "role_id": user.role_id,
# #             "created_at": user.created_at.isoformat()
# #         }), 200
# #
# #     @staticmethod
# #     def update(user_id, data, db):
# #
# #         user = UserService.get_user_by_id(db, user_id)
# #
# #         if not user:
# #             return jsonify({"message": "User not found"}), 404
# #
# #         if "password" in data:
# #             data["password_hash"] = hash_password(data["password"])
# #             del data["password"]
# #
# #         updated_user, error = UserService.update_user(db, user, data)
# #
# #         if error:
# #             return jsonify({"message": error}), 400
# #
# #         return jsonify({
# #             "id": updated_user.id,
# #             "username": updated_user.username,
# #             "email": updated_user.email,
# #             "phone": updated_user.phone,
# #             "address": updated_user.address,
# #             "role_id": updated_user.role_id,
# #             "updated_at": updated_user.updated_at.isoformat()
# #         }), 200
# #
# #     @staticmethod
# #     def delete(user_id, db):
# #
# #         user = UserService.get_user_by_id(db, user_id)
# #
# #         if not user:
# #             return jsonify({"message": "User not found"}), 404
# #
# #         UserService.delete_user(db, user)
# #
# #         return jsonify({"message": "User deleted"}), 200