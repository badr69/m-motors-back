from flask import jsonify, request
from typing import Dict, Any
from app.core.db import SessionLocal
from app.modules.users.service import UserService


class UserController:

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    def create_user():
        db = SessionLocal()
        try:
            data: Dict[str, Any] = request.get_json() or {}

            result = UserService.create_user(db, data)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "User created successfully",
                "data": result["data"]
            }), 201

        finally:
            db.close()

    # =====================
    # GET ALL USERS
    # =====================
    @staticmethod
    def get_users():
        db = SessionLocal()
        try:
            result = UserService.get_users(db)

            return jsonify({
                "message": "Users retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # GET USER BY ID (FIXED)
    # =====================
    @staticmethod
    def get_user_by_id(user_id):
        db = SessionLocal()
        try:
            current_user = getattr(request, "current_user", None)

            result = UserService.get_user_by_id(db, current_user, user_id)

            if result["error"] == "Forbidden":
                return jsonify({"message": "Forbidden"}), 403

            if result["error"] == "User not found":
                return jsonify({"message": "User not found"}), 404

            return jsonify({
                "message": "User retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update_user(user_id):
        db = SessionLocal()
        try:
            data: Dict[str, Any] = request.get_json() or {}

            result = UserService.update_user(db, user_id, data)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "User updated successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete_user(user_id):
        db = SessionLocal()
        try:
            result = UserService.delete_user(db, user_id)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 404

            return jsonify({
                "message": result["data"]["message"]
            }), 200

        finally:
            db.close()

    # =====================
    # ME
    # =====================
    @staticmethod
    def get_me():
        db = SessionLocal()
        try:
            current_user = getattr(request, "current_user", None)

            if not current_user:
                return jsonify({"message": "Unauthorized"}), 401

            result = UserService.get_me(db, current_user)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 404

            return jsonify({
                "message": "Current user retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    @staticmethod
    def update_me():
        db = SessionLocal()
        try:

            current_user = getattr(request, "current_user", None)
            data = request.get_json() or {}

            if not isinstance(current_user, dict):
                return jsonify({"message": "Invalid token payload"}), 401

            result = UserService.update_me(db, current_user, data)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "User updated successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # @staticmethod
    # def update_me():
    #     db = SessionLocal()
    #     try:

            # current_user = getattr(request, "current_user", None)
            # data = request.get_json() or {}
            #
            # result = UserService.update_me(db, current_user, data)
            # current_user = getattr(request, "current_user", None)
            #
            # if not current_user:
            #     return jsonify({"message": "Unauthorized"}), 401
            #
            # user_id = current_user.get("user_id")
            #
            # result = UserService.update_me(db, user_id, data)
            #
            # if result.get("error"):
            #     return jsonify({"message": result["error"]}), 400

            # =========================
            # ACTIVE VERSION FIXED
            # =========================

            # current_user = getattr(request, "current_user", None)
            #
            # if not isinstance(current_user, dict):
            #     return jsonify({"message": "Invalid token payload"}), 401
            #
            # user_id = current_user.get("user_id")
            #
            # if not user_id:
            #     return jsonify({"message": "Missing user_id"}), 401
            #
            # # 🔥 MISSING PART (CRITICAL FIX)
            # data = request.get_json() or {}
            #
            # result = UserService.update_me(db, user_id, data)
            #
            # if result.get("error"):
            #     return jsonify({"message": result["error"]}), 400
            #
            # return jsonify({
            #     "message": "User updated successfully",
        #         "data": result["data"]
        #     }), 200
        #
        # finally:
        #     db.close()

    @staticmethod
    def delete_me():
        db = SessionLocal()
        try:
            current_user = getattr(request, "current_user", None)

            result = UserService.delete_me(db, current_user)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 404

            return jsonify({
                "message": result["data"]["message"]
            }), 200

        finally:
            db.close()





















# from flask import jsonify, request
# from typing import Dict, Any
# from app.core.db import SessionLocal
# from app.modules.users.service import UserService
#
#
# class UserController:
#
#     # =====================
#     # CREATE USER
#     # =====================
#     @staticmethod
#     def create_user():
#
#         db = SessionLocal()
#         try:
#             data: Dict[str, Any] = request.get_json() or {}
#             print("🔥 [DEBUG] CREATE USER REQUEST DATA:", data)
#
#             result = UserService.create_user(db, data)
#
#             if result.get("error"):
#                 return jsonify({"message": result["error"]}), 400
#
#             return jsonify({
#                 "message": "User created successfully",
#                 "data": result["data"]
#             }), 201
#
#         finally:
#             db.close()
#
#     # =====================
#     # GET ALL USERS
#     # =====================
#     @staticmethod
#     def get_users():
#
#         db = SessionLocal()
#         try:
#             result = UserService.get_users(db)
#
#             return jsonify({
#                 "message": "Users retrieved successfully",
#                 "data": result["data"]
#             }), 200
#
#         finally:
#             db.close()
#
#     # =====================
#     # GET USER BY ID
#     # =====================
#     @staticmethod
#     def get_user_by_id(user_id):
#
#         db = SessionLocal()
#         try:
#             result = UserService.get_user_by_id(db, user_id)
#
#             if result.get("error"):
#                 return jsonify({"message": result["error"]}), 404
#
#             return jsonify({
#                 "message": "User retrieved successfully",
#                 "data": result["data"]
#             }), 200
#
#         finally:
#             db.close()
#
#     # =====================
#     # UPDATE USER
#     # =====================
#     @staticmethod
#     def update_user(user_id):
#
#         db = SessionLocal()
#         try:
#             data: Dict[str, Any] = request.get_json() or {}
#
#             result = UserService.update_user(db, user_id, data)
#
#             if result.get("error"):
#                 return jsonify({"message": result["error"]}), 400
#
#             return jsonify({
#                 "message": "User updated successfully",
#                 "data": result["data"]
#             }), 200
#
#         finally:
#             db.close()
#
#     # =====================
#     # DELETE USER
#     # =====================
#     @staticmethod
#     def delete_user(user_id):
#
#         db = SessionLocal()
#         try:
#             result = UserService.delete_user(db, user_id)
#
#             if result.get("error"):
#                 return jsonify({"message": result["error"]}), 404
#
#             return jsonify({
#                 "message": result["data"]["message"]
#             }), 200
#
#         finally:
#             db.close()
#
#     # =====================
#     # GET ME
#     # =====================
#     @staticmethod
#     def get_me():
#
#         db = SessionLocal()
#
#         try:
#             current_user = getattr(request, "current_user", None)
#
#             if not current_user:
#                 return jsonify({"message": "Unauthorized"}), 401
#
#             result = UserService.get_me(db, current_user)
#
#             if result.get("error"):
#                 return jsonify({"message": result["error"]}), 401
#
#             return jsonify({
#                 "message": "Current user retrieved successfully",
#                 "data": result["data"]
#             }), 200
#
#         finally:
#             db.close()
#
#     # =====================
#     # UPDATE ME
#     # =====================
#     @staticmethod
#     def update_me():
#
#         db = SessionLocal()
#         try:
#             current_user: Dict[str, Any] = getattr(request, "current_user", {}) or {}
#             data: Dict[str, Any] = request.get_json() or {}
#
#             result = UserService.update_me(db, current_user, data)
#
#             if result.get("error"):
#                 return jsonify({"message": result["error"]}), 400
#
#             return jsonify({
#                 "message": "User updated successfully",
#                 "data": result["data"]
#             }), 200
#
#         finally:
#             db.close()
#
#     # =====================
#     # DELETE ME
#     # =====================
#     @staticmethod
#     def delete_me():
#
#         db = SessionLocal()
#         try:
#             current_user: Dict[str, Any] = getattr(request, "current_user", {}) or {}
#
#             result = UserService.delete_me(db, current_user)
#
#             if result.get("error"):
#                 return jsonify({"message": result["error"]}), 404
#
#             return jsonify({
#                 "message": result["data"]["message"]
#             }), 200
#
#         finally:
#             db.close()