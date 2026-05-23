from sqlalchemy.orm import Session
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
    @staticmethod
    def get_users():

        db = SessionLocal()
        try:
            return db.query(User).all()
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
    def update_user(user_id: int, data: dict, current_user):

        db = SessionLocal()

        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, "User not found"

            # =====================
            # ADMIN PROTECTION
            # =====================
            if user.role.name.lower() == "admin":
                return None, "ADMIN user cannot be modified"

            # =====================
            # NORMAL USER RESTRICTION
            # =====================
            if current_user.role.name.lower() != "admin" and current_user.id != user_id:
                return None, "Forbidden"

            for key, value in data.items():
                setattr(user, key, value)

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
    def delete_user(user_id: int, current_user):

        db = SessionLocal()

        try:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return False, "User not found"

            # =====================
            # PROTECTION ADMIN
            # =====================
            if user.role.name.lower() == "admin":
                return False, "ADMIN user cannot be deleted"

            # =====================
            # PROTECTION USER (optionnel mais propre)
            # =====================
            if current_user.role.name.lower() != "admin" and current_user.id != user_id:
                return False, "Forbidden"

            db.delete(user)
            db.commit()

            return True, None

        finally:
            db.close()

    # =====================
    # GET CURRENT USER (ME)
    # =====================
    @staticmethod
    def get_me(current_user):

        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "phone": current_user.phone,
            "address": current_user.address,
            "role": current_user.role.name
        }, None

    # =====================
    # UPDATE CURRENT USER (ME)
    # =====================
    @staticmethod
    def update_me(current_user, data, db):

        user = db.query(User).filter(User.id == current_user.id).first()

        if not user:
            return None, "User not found"

        for key, value in data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        }, None

    # =====================
    # DELETE CURRENT USER (ME)
    # =====================
    @staticmethod
    def delete_me(current_user, db):

        user = db.query(User).filter(User.id == current_user.id).first()

        if not user:
            return False, "User not found"

        db.delete(user)
        db.commit()

        return True, None
