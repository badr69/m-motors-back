from flask import jsonify, request
from app.modules.auth.service import AuthService
from app.core.db import SessionLocal
from app.core.security.jwt_middleware import jwt_required


class AuthController:

    # =====================
    # REGISTER
    # =====================
    @staticmethod
    def register():
        db = SessionLocal()
        try:
            data = request.get_json() or {}

            result, error = AuthService.register(db, data)

            if error:
                return jsonify({"message": error}), 400

            return jsonify(result), 201

        finally:
            db.close()

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login():
        db = SessionLocal()
        try:
            data = request.get_json() or {}

            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return jsonify({"message": "Email and password required"}), 400

            result, error = AuthService.login(db, email, password)

            if error:
                return jsonify({"message": error}), 401

            return jsonify(result), 200

        finally:
            db.close()

    # =====================
    # REFRESH TOKEN
    # =====================
    @staticmethod
    def refresh():
        db = SessionLocal()
        try:
            auth_header = request.headers.get("Authorization")

            result, error = AuthService.refresh_token(db, auth_header)

            if error:
                return jsonify({"message": error}), 401

            return jsonify(result), 200

        finally:
            db.close()

    # =====================
    # CURRENT USER (PROTECTED)
    # =====================
    @staticmethod
    @jwt_required
    def current_user():
        db = SessionLocal()
        try:
            user_id = request.user_id

            result, error = AuthService.current_user(db, user_id)

            if error:
                return jsonify({"message": error}), 401

            return jsonify(result), 200

        finally:
            db.close()

    # =====================
    # LOGOUT
    # =====================
    @staticmethod
    def logout():
        return jsonify(AuthService.logout()), 200