from flask import jsonify, request
from app.modules.auth.service import AuthService
from app.core.db import SessionLocal


class AuthController:

    # =====================
    # REGISTER
    # =====================
    @staticmethod
    def register():
        db = SessionLocal()
        try:
            data = request.get_json()

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
            data = request.get_json()

            result, error = AuthService.login(
                db,
                data.get("email"),
                data.get("password")
            )

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
    # CURRENT USER
    # =====================
    @staticmethod
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