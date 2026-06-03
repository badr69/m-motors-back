from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import verify_password, hash_password
from app.core.security.jwt import (
    generate_access_token,
    generate_refresh_token,
    decode_token
)


class AuthService:

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login(email, password):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            print("USER:", user)
            print("ROLE:", user.role)
            print("ROLE NAME:", getattr(user.role, "name", None))

            if not user:
                return None, "User not found"

            if hasattr(user, "is_active") and user.is_active is False:
                return None, "Account disabled"

            if not verify_password(password, user.password_hash):
                return None, "Invalid password"

            role_name = user.role.name.upper() if user.role else "CLIENT"

            return {
                "access_token": generate_access_token(user),
                "refresh_token": generate_refresh_token(user),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": role_name
                }
            }, None

        finally:
            db.close()

    # =====================
    # REGISTER
    # =====================
    @staticmethod
    def register(data):

        db = SessionLocal()
        try:
            if db.query(User).filter(User.email == data.get("email")).first():
                return None, "Email already exists"

            if db.query(User).filter(User.username == data.get("username")).first():
                return None, "Username already exists"

            role = db.query(Role).filter(Role.name == "CLIENT").first()

            if not role:
                return None, "CLIENT role not found"

            user = User(
                username=data.get("username"),
                email=data.get("email"),
                phone=data.get("phone"),
                address=data.get("address"),
                password_hash=hash_password(data.get("password")),
                role_id=role.id
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            return {
                "message": "Register successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "address": user.address,
                    "role": role.name.upper()
                }
            }, None

        finally:
            db.close()

    # =====================
    # CURRENT USER
    # =====================
    @staticmethod
    def current_user(user_id):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            role_name = user.role.name.upper() if user.role else "CLIENT"

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role": role_name
            }, None

        finally:
            db.close()

    # =====================
    # REFRESH TOKEN
    # =====================
    @staticmethod
    def refresh_token(auth_header):

        if not auth_header:
            return None, "Token missing"

        try:
            token = auth_header.split(" ")[1]
            payload = decode_token(token)

            if payload.get("type") != "refresh":
                return None, "Invalid token type"

            user_id = payload.get("user_id")

            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()

                if not user:
                    return None, "User not found"

                return {
                    "access_token": generate_access_token(user)
                }, None

            finally:
                db.close()

        except Exception:
            return None, "Invalid or expired token"

    # =====================
    # LOGOUT
    # =====================
    @staticmethod
    def logout():
        return {
            "message": "Logged out successfully"
        }, None