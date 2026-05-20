from app.core.db import SessionLocal
from app.modules.users.model import User
from app.core.security.jwt import (
    generate_access_token,
    generate_refresh_token,
    decode_token
)
from app.core.security.password import verify_password


class AuthService:

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login(email: str, password: str):

        db = SessionLocal()

        try:
            user = db.query(User).filter(User.email == email).first()

            if not user:
                return None, "User not found"

            if not verify_password(password, user.password):
                return None, "Invalid password"

            return {
                "access_token": generate_access_token(user),
                "refresh_token": generate_refresh_token(user),
                "user": {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": getattr(user.role, "name", "USER")
                }
            }, None

        finally:
            db.close()

    # =====================
    # REFRESH TOKEN
    # =====================
    @staticmethod
    def refresh_token(auth_header):

        db = SessionLocal()

        try:
            if not auth_header:
                return None, "Token missing"

            token = auth_header.split(" ")[1]
            payload = decode_token(token)

            if payload.get("type") != "refresh":
                return None, "Invalid token type"

            user = db.query(User).filter(
                User.id == payload.get("user_id")
            ).first()

            if not user:
                return None, "User not found"

            return {
                "access_token": generate_access_token(user)
            }, None

        except Exception:
            return None, "Invalid or expired token"

        finally:
            db.close()

    # =====================
    # LOGOUT
    # =====================
    @staticmethod
    def logout():
        return {"message": "Logged out successfully"}

    # =====================
    # CURRENT USER
    # =====================
    @staticmethod
    def current_user(auth_header):

        db = SessionLocal()

        try:
            if not auth_header:
                return None, "Token missing"

            token = auth_header.split(" ")[1]
            payload = decode_token(token)

            user = db.query(User).filter(
                User.id == payload.get("user_id")
            ).first()

            if not user:
                return None, "User not found"

            return {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": getattr(user.role, "name", "USER")
            }, None

        finally:
            db.close()