from sqlalchemy.orm import Session
from app.modules.users.model import User
from app.modules.roles.model import Role
from typing import Dict, Any


class UserService:

    # =====================
    # HELPERS
    # =====================
    @staticmethod
    def _is_admin(user: User) -> bool:
        return user.role and user.role.name.upper() == "ADMIN"

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    def create_user(db: Session, user_data: Dict[str, Any]):

        role_id = user_data.get("role_id")

        role = db.query(Role).filter(Role.id == role_id).first()

        if not role:
            return None, "Role not found"

        if role.name.upper() == "ADMIN":
            return None, "Cannot assign ADMIN role"

        user = User(
            username=user_data.get("username"),
            email=user_data.get("email"),
            password_hash=user_data.get("password_hash"),
            phone=user_data.get("phone"),
            address=user_data.get("address"),
            role_id=role_id
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user, None

    # =====================
    # READ ALL USERS
    # =====================
    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    # =====================
    # GET USER BY ID
    # =====================
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # =====================
    # GET BY EMAIL
    # =====================
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    # =====================
    # GET BY USERNAME
    # =====================
    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update_user(db: Session, user: User, data: Dict[str, Any]):

        # PROTECT ADMIN
        if UserService._is_admin(user):
            return None, "Cannot modify admin user"

        allowed_fields = [
            "username",
            "email",
            "phone",
            "address",
            "password_hash"
        ]

        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        db.commit()
        db.refresh(user)

        return user, None

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete_user(db: Session, user: User):

        if UserService._is_admin(user):
            return False, "Cannot delete admin user"

        db.delete(user)
        db.commit()

        return True, None