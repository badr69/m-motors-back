from flask import jsonify
from app.modules.auth.service import AuthService


class AuthController:

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login(data):

        result, error = AuthService.login(
            data.get("email"),
            data.get("password")
        )

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200

    # =====================
    # REFRESH
    # =====================
    @staticmethod
    def refresh(auth_header):

        result, error = AuthService.refresh_token(auth_header)

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200

    # =====================
    # LOGOUT
    # =====================
    @staticmethod
    def logout():
        return jsonify(AuthService.logout()), 200

    # =====================
    # CURRENT USER
    # =====================
    @staticmethod
    def current_user(auth_header):

        result, error = AuthService.current_user(auth_header)

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200