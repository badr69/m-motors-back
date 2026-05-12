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
    def login(db, email: str, password: str):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None, "Invalid credentials"

        if not user.is_active:
            return None, "Account disabled"

        # sécurité supplémentaire
        if not user.password_hash:
            return None, "Invalid credentials"

        # protection crash hash
        try:
            valid = verify_password(password, user.password_hash)
        except Exception:
            return None, "Invalid credentials"

        if not valid:
            return None, "Invalid credentials"

        # rôle safe
        role = "USER"
        try:
            if user.role:
                role = user.role.name
        except Exception:
            role = "USER"

        return {
            "access_token": generate_access_token(user),
            "refresh_token": generate_refresh_token(user),

            "user": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role
            }
        }, None

    # =====================
    # REFRESH TOKEN
    # =====================
    @staticmethod
    def refresh_token(db, auth_header):

        if not auth_header:
            return None, "Token missing"

        try:
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
    def current_user(db, user_id):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None, "User not found"

        role = "USER"
        try:
            if user.role:
                role = user.role.name
        except:
            pass

        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role
        }, None