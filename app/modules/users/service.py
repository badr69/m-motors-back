from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from typing import Dict, Any
from app.core.security.password import hash_password
from sqlalchemy.orm import joinedload


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
    @staticmethod
    def get_users():

        db = SessionLocal()
        try:
            return (
                db.query(User)
                .options(joinedload(User.role))
                .all()
            )
        finally:
            db.close()


    # =====================
    # GET BY ID
    # =====================
    @staticmethod
    def get_user_by_id(user_id: int):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            return user, None
        finally:
            db.close()


    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update_user(user_id: int, data: Dict[str, Any]):

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            if "password" in data:
                data["password_hash"] = hash_password(data["password"])
                del data["password"]

            for key, value in data.items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)

            return user, None

        finally:
            db.close()


    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete_user(user_id: int):

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

