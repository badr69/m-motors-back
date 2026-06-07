from flask import request, jsonify
from app.core.db import SessionLocal
from app.modules.auth.service import AuthService


class AuthController:

    @staticmethod
    def login():
        db = SessionLocal()

        try:
            data = request.get_json() or {}
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return jsonify({"message": "Email and password required"}), 400

            result = AuthService.login(db, email, password)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 401

            return jsonify(result.get("data")), 200

        finally:
            db.close()


    @staticmethod
    def register():
        db = SessionLocal()

        try:
            data = request.get_json() or {}
            result = AuthService.register(db, data)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 400

            return jsonify(result.get("data")), 201

        finally:
            db.close()


    @staticmethod
    def refresh():
        db = SessionLocal()

        try:
            auth_header = request.headers.get("Authorization")

            result = AuthService.refresh_token(db, auth_header)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 401

            return jsonify(result.get("data")), 200

        finally:
            db.close()


    @staticmethod
    def current_user():
        db = SessionLocal()

        try:
            current_user = getattr(request, "current_user", None)

            if not current_user:
                return jsonify({"message": "Unauthorized"}), 401

            user_id = current_user.get("user_id")

            result = AuthService.current_user(db, user_id)

            if result.get("error"):
                return jsonify({"message": result["error"]}), 401

            return jsonify(result.get("data")), 200

        finally:
            db.close()


    @staticmethod
    def logout():
        result = AuthService.logout()
        return jsonify(result.get("data")), 200