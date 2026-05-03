# roles/service.py
from app.modules.roles.model import Role


class RoleService:

    @staticmethod
    def create_role(db, name: str):

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

    @staticmethod
    def get_roles(db):
        return db.query(Role).all()

    @staticmethod
    def get_role_by_id(db, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def update_role(db, role, name: str):

        if not name or name.strip() == "":
            return None, "Name is required"

        role.name = name.strip()
        db.commit()
        db.refresh(role)

        return role, None

    @staticmethod
    def delete_role(db, role):
        db.delete(role)
        db.commit()