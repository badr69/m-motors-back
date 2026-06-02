from flask import request, jsonify, g
from app.modules.auth.service import AuthService


class AuthController:

    @staticmethod
    def register():

        data = request.get_json() or {}

        result, error = AuthService.register(data)

        if error:
            return jsonify({"message": error}), 400

        return jsonify(result), 201

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

    @staticmethod
    def current_user():

        user = getattr(g, "current_user", None)

        if not user:
            return jsonify({"message": "Unauthorized"}), 401

        return jsonify(user), 200

    @staticmethod
    def logout():
        result, _ = AuthService.logout()
        return jsonify(result), 200