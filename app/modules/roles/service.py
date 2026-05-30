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

            role_name = name.strip().lower()

            existing = db.query(Role).filter(Role.name == role_name).first()

            if existing:
                return None, "Role already exists"

            role = Role(name=role_name)

            db.add(role)
            db.commit()
            db.refresh(role)

            return {
                "id": role.id,
                "name": role.name,
                "created_at": role.created_at.isoformat(),
                "updated_at": role.updated_at.isoformat()
            }, None

        finally:
            db.close()

    # =====================
    # GET ALL
    # =====================
    @staticmethod
    def get_roles():

        db = SessionLocal()

        try:

            roles = db.query(Role).all()

            return [
                {
                    "id": r.id,
                    "name": r.name,
                    "created_at": r.created_at.isoformat(),
                    "updated_at": r.updated_at.isoformat()
                }
                for r in roles
            ]

        finally:
            db.close()

    # =====================
    # GET ONE
    # =====================
    @staticmethod
    def get_role_by_id(role_id: int):

        db = SessionLocal()

        try:

            role = db.query(Role).filter(Role.id == role_id).first()

            if not role:
                return None, "Role not found"

            return {
                "id": role.id,
                "name": role.name,
                "created_at": role.created_at.isoformat(),
                "updated_at": role.updated_at.isoformat()
            }, None

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

            if role.name.lower() == "admin":
                return None, "ADMIN role cannot be modified"

            if not name or name.strip() == "":
                return None, "Name is required"

            role.name = name.strip().lower()

            db.commit()
            db.refresh(role)

            return {
                "id": role.id,
                "name": role.name,
                "created_at": role.created_at.isoformat(),
                "updated_at": role.updated_at.isoformat()
            }, None

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
                return False, "Role not found"

            if role.name.lower() == "admin":
                return False, "ADMIN role cannot be deleted"

            db.delete(role)
            db.commit()

            return True, None

        finally:
            db.close()
