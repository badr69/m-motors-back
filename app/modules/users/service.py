from sqlalchemy.orm import joinedload
from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from typing import Dict, Any
from app.core.security.password import hash_password


class UserService:

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    def create_user(data: Dict[str, Any]):

        db = SessionLocal()
        try:
            role = db.query(Role).filter(Role.id == data.get("role_id")).first()

            if not role:
                return None, "Role not found"

            user = User(
                username=data.get("username"),
                email=data.get("email"),
                password_hash=hash_password(data.get("password")),
                phone=data.get("phone"),
                address=data.get("address"),
                role_id=data.get("role_id")
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            return user, None

        finally:
            db.close()

    # =====================
    # GET ALL USERS
    # =====================
    from sqlalchemy.orm import joinedload
    @staticmethod
    def get_users():
        db = SessionLocal()
        try:
            users = db.query(User) \
                .options(joinedload(User.role)) \
                .order_by(User.id.asc()) \
                .all()

            return users
        finally:
            db.close()

    # =====================
    # GET BY ID
    # =====================
    @staticmethod
    def get_user_by_id(user_id):
        db = SessionLocal()
        try:
            user = db.query(User) \
                .options(joinedload(User.role)) \
                .filter(User.id == user_id) \
                .first()

            if not user:
                return None, "User not found"

            return user, None

        finally:
            db.close()
    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update_user(user_id: int, data: dict, current_user: dict):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            # =====================
            # CURRENT USER FROM TOKEN
            # =====================
            current_user_id = current_user.get("user_id")
            current_user_role = (current_user.get("role") or "").lower()

            # =====================
            # ADMIN PROTECTION
            # =====================
            if user.role and user.role.name.lower() == "admin":
                return None, "ADMIN user cannot be modified"

            # =====================
            # PERMISSION CHECK
            # =====================
            if current_user_role != "admin" and current_user_id != user_id:
                return None, "Forbidden"

            # =====================
            # SAFE UPDATE (WHITELIST)
            # =====================
            allowed_fields = ["username", "email", "phone", "address"]

            for key, value in data.items():
                if key in allowed_fields:
                    setattr(user, key, value)

            # =====================
            # PASSWORD UPDATE
            # =====================
            if data.get("password"):
                user.password_hash = hash_password(data["password"])

            # =====================
            # ROLE UPDATE ONLY ADMIN
            # =====================
            if current_user_role == "admin" and data.get("role_id"):
                user.role_id = data["role_id"]

            db.commit()
            db.refresh(user)

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, None

        finally:
            db.close()

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete_user(user_id: int, current_user: dict):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return False, "User not found"

            current_user_id = current_user.get("user_id")
            current_user_role = (current_user.get("role") or "").lower()

            # ADMIN PROTECTION
            if user.role and user.role.name.lower() == "admin":
                return False, "ADMIN user cannot be deleted"

            # PERMISSION CHECK
            if current_user_role != "admin" and current_user_id != user_id:
                return False, "Forbidden"

            db.delete(user)
            db.commit()

            return True, None

        finally:
            db.close()

    # =====================
    # GET ME
    # =====================
    @staticmethod
    def get_me(user_id):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role": user.role.name if user.role else None
            }, None

        finally:
            db.close()

    # =====================
    # UPDATE ME
    # =====================
    @staticmethod
    def update_me(user_id, data):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            allowed_fields = ["username", "phone", "address"]

            for key, value in data.items():
                if key in allowed_fields:
                    setattr(user, key, value)

            if data.get("password"):
                user.password_hash = hash_password(data["password"])

            db.commit()
            db.refresh(user)

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address
            }, None

        finally:
            db.close()

    # =====================
    # DELETE ME
    # =====================
    @staticmethod
    def delete_me(user_id):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return False, "User not found"

            db.delete(user)
            db.commit()

            return True, None

        finally:
            db.close()
