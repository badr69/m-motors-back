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
    def login(db, email, password):

        if not email or not password:
            return {"data": None, "error": "Email and password required"}

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return {"data": None, "error": "User not found"}

        if not user.is_active:
            return {"data": None, "error": "Account disabled"}

        if not verify_password(password, user.password_hash):
            return {"data": None, "error": "Invalid password"}

        return AuthService._build_auth_response(user)

    # =====================
    # REGISTER
    # =====================
    @staticmethod
    def register(db, data):

        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        if not email or not username or not password:
            return {"data": None, "error": "Missing required fields"}

        if db.query(User).filter(User.email == email).first():
            return {"data": None, "error": "Email already exists"}

        if db.query(User).filter(User.username == username).first():
            return {"data": None, "error": "Username already exists"}

        role = db.query(Role).filter(Role.name == "CLIENT").first()

        if not role:
            return {"data": None, "error": "CLIENT role not found"}

        user = User(
            username=username,
            email=email,
            phone=data.get("phone"),
            address=data.get("address"),
            password_hash=hash_password(password),
            role_id=role.id,
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return AuthService._build_auth_response(user, role.name)

    # =====================
    # CURRENT USER
    # =====================
    @staticmethod
    def current_user(db, user_id):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {"data": None, "error": "User not found"}

        return {
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role": user.role.name.upper() if user.role else "CLIENT"
            },
            "error": None
        }

    # =====================
    # REFRESH TOKEN
    # =====================
    @staticmethod
    def refresh_token(db, token):

        if not token:
            return {"data": None, "error": "Token missing"}

        payload = decode_token(token, expected_type="refresh")

        if not payload:
            return {"data": None, "error": "Invalid refresh token"}

        user_id = payload.get("user_id")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {"data": None, "error": "User not found"}

        return {
            "data": {
                "access_token": generate_access_token(user)
            },
            "error": None
        }

    # =====================
    # LOGOUT
    # =====================
    @staticmethod
    def logout():
        return {"data": {"message": "Logged out successfully"}, "error": None}

    # =====================
    # PRIVATE
    # =====================
    @staticmethod
    def _build_auth_response(user, role_name=None):

        role = role_name or (user.role.name if user.role else "CLIENT")

        return {
            "data": {
                "access_token": generate_access_token(user),
                "refresh_token": generate_refresh_token(user),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": role.upper()
                }
            },
            "error": None
        }