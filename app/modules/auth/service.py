from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import verify_password, hash_password
from app.core.security.jwt import generate_access_token, generate_refresh_token


class AuthService:

    # =====================
    # REGISTER
    # =====================
    @staticmethod
    def register(data):

        db = SessionLocal()
        try:
            email = data.get("email")
            username = data.get("username")
            password = data.get("password")

            if not email or not username or not password:
                return None, "Missing fields"

            if db.query(User).filter(User.email == email).first():
                return None, "Email already exists"

            if db.query(User).filter(User.username == username).first():
                return None, "Username already exists"

            role = db.query(Role).filter(Role.name == "CLIENT").first()

            if not role:
                return None, "CLIENT role not found"

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

            return {
                "message": "Register successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": "CLIENT"
                }
            }, None

        finally:
            db.close()

    # =====================
    # LOGIN
    # =====================
    @staticmethod
    def login(email, password):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()

            if not user:
                # return None, "Invalid credentials"
                return None, "User not found"

            if not verify_password(password, user.password_hash):
                # return None, "Invalid credentials"
                return None, "Invalid password"

            role_name = (user.role.name if user.role else "CLIENT").upper().strip()

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
    # CURRENT USER (OPTION DB)
    # =====================
    @staticmethod
    def current_user(user_id):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            role_name = (user.role.name if user.role else "CLIENT").upper().strip()

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role_name
            }, None

        finally:
            db.close()

    # =====================
    # LOGOUT
    # =====================
    @staticmethod
    def logout():
        return {"message": "Logged out successfully"}, None