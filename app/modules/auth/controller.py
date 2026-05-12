from flask import jsonify
from app.modules.auth.service import AuthService


class AuthController:

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login(data, db):
        email = data.get("email")
        password = data.get("password")

        result, error = AuthService.login(db, email, password)

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200

    # =====================
    # REFRESH
    # =====================
    @staticmethod
    def refresh(db, auth_header):
        result, error = AuthService.refresh_token(db, auth_header)

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
    def current_user(db, user_id):
        result, error = AuthService.current_user(db, user_id)

        if error:
            return jsonify({"message": error}), 401

        return jsonify(result), 200