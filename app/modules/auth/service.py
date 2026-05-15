from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.jwt import (
    generate_access_token,
    generate_refresh_token,
    decode_token
)
from app.core.security.password import (
    verify_password,
    hash_password
)


class AuthService:

    # =====================
    # REGISTER
    # =====================
    @staticmethod
    def register(db, data):

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
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role.name.upper()
            }
        }, None

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login(db, email, password):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return None, "Invalid credentials"

        if not user.is_active:
            return None, "Account disabled"

        try:
            if not verify_password(password, user.password_hash):
                return None, "Invalid credentials"
        except:
            return None, "Invalid credentials"

        role = user.role.name.upper() if user.role else "CLIENT"

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

            user = db.query(User).filter(User.id == payload.get("user_id")).first()

            if not user:
                return None, "User not found"

            return {
                "access_token": generate_access_token(user)
            }, None

        except:
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

        role = user.role.name.upper() if user.role else "CLIENT"

        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role
        }, None