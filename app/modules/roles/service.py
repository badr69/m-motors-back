from app.core.db import SessionLocal
from app.modules.roles.model import Role


class RoleService:

    # =====================
    # CREATE ROLE
    # =====================
    @staticmethod
    def create_role(name: str):

        db = SessionLocal()

        try:
            if not name or name.strip() == "":
                return None, "Name is required"

            role_name = name.strip().upper()

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
                "created_at": role.created_at.isoformat() if role.created_at else None,
                "updated_at": role.updated_at.isoformat() if role.updated_at else None
            }, None

        except Exception as e:
            db.rollback()
            print("[ROLE CREATE ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # GET ALL ROLES
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
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "updated_at": r.updated_at.isoformat() if r.updated_at else None
                }
                for r in roles
            ], None

        except Exception as e:
            print("[ROLE GET ALL ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # GET ROLE BY ID
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
                "created_at": role.created_at.isoformat() if role.created_at else None,
                "updated_at": role.updated_at.isoformat() if role.updated_at else None
            }, None

        except Exception as e:
            print("[ROLE GET ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # UPDATE ROLE
    # =====================
    @staticmethod
    def update_role(role_id: int, name: str):

        db = SessionLocal()

        try:
            role = db.query(Role).filter(Role.id == role_id).first()

            if not role:
                return None, "Role not found"

            if role.name.upper() == "ADMIN":
                return None, "ADMIN role cannot be modified"

            if not name or name.strip() == "":
                return None, "Name is required"

            role.name = name.strip().upper()

            db.commit()
            db.refresh(role)

            return {
                "id": role.id,
                "name": role.name,
                "created_at": role.created_at.isoformat() if role.created_at else None,
                "updated_at": role.updated_at.isoformat() if role.updated_at else None
            }, None

        except Exception as e:
            db.rollback()
            print("[ROLE UPDATE ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # DELETE ROLE
    # =====================
    @staticmethod
    def delete_role(role_id: int):

        db = SessionLocal()

        try:
            role = db.query(Role).filter(Role.id == role_id).first()

            if not role:
                return False, "Role not found"

            if role.name.upper() == "ADMIN":
                return False, "ADMIN role cannot be deleted"

            db.delete(role)
            db.commit()

            return True, None

        finally:
            db.close()
