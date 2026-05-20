# roles/service.py
from app.core.db import SessionLocal
from app.modules.roles.model import Role


class RoleService:

    # =====================
    # CREATE
    # =====================
    @staticmethod
    def create_role(name: str):

        db = SessionLocal()

        try:

            if not name or name.strip() == "":
                return None, "Name is required"

            existing = db.query(Role).filter(Role.name == name).first()

            if existing:
                return None, "Role already exists"

            role = Role(name=name.strip())

            db.add(role)
            db.commit()
            db.refresh(role)

            return role, None

        finally:
            db.close()

    # =====================
    # GET ALL
    # =====================
    @staticmethod
    def get_roles():

        db = SessionLocal()

        try:
            return db.query(Role).all()

        finally:
            db.close()

    # =====================
    # GET ONE
    # =====================
    @staticmethod
    def get_role_by_id(role_id: int):

        db = SessionLocal()

        try:
            return db.query(Role).filter(Role.id == role_id).first()

        finally:
            db.close()

    # =====================
    # UPDATE
    # =====================
    @staticmethod
    def update_role(role_id: int, name: str):

        db = SessionLocal()

        try:

            role = db.query(Role).filter(Role.id == role_id).first()

            if not role:
                return None, "Role not found"

            if not name or name.strip() == "":
                return None, "Name is required"

            role.name = name.strip()

            db.commit()
            db.refresh(role)

            return role, None

        finally:
            db.close()

    # =====================
    # DELETE
    # =====================
    @staticmethod
    def delete_role(role_id: int):

        db = SessionLocal()

        try:

            role = db.query(Role).filter(Role.id == role_id).first()

            if not role:
                return "Role not found"

            db.delete(role)
            db.commit()

            return None

        finally:
            db.close()