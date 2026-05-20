from flask import request, jsonify
from app.modules.auth.service import AuthService


class AuthController:

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login():
        data = request.get_json() or {}

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email and password required"}), 400

        result, error = AuthService.login(email, password)

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200


    # =====================
    # REGISTER
    # =====================
    @staticmethod
    def register():
        data = request.get_json() or {}

        result, error = AuthService.register(data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify(result), 201


    # =====================
    # REFRESH
    # =====================
    @staticmethod
    def refresh():
        auth_header = request.headers.get("Authorization")

        result, error = AuthService.refresh_token(auth_header)

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200


    # =====================
    # CURRENT USER
    # =====================
    @staticmethod
    def current_user():

        user_id = getattr(request, "user_id", None)

        if not user_id:
            return jsonify({"message": "Unauthorized"}), 401

        result, error = AuthService.current_user(user_id)

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200


    # =====================
    # LOGOUT
    # =====================
    @staticmethod
    def logout():
        return jsonify(AuthService.logout()), 200