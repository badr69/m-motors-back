from app.modules.roles.model import Role
from app.core.logger import setup_logger

logger = setup_logger("role-service")


class RoleService:

    # =====================
    # NORMALIZE (ONLY LOWERCASE)
    # =====================
    @staticmethod
    def normalize(role: str) -> str:
        if not role:
            return None

        return role.strip().lower()

    # =====================
    # CREATE ROLE
    # =====================
    @staticmethod
    def create_role(db, name: str):

        logger.info(f"Creating role: {name}")

        if not name or name.strip() == "":
            return {"data": None, "error": "Name is required"}

        role_name = RoleService.normalize(name)

        existing = db.query(Role).filter(
            Role.name == role_name
        ).first()

        if existing:
            return {"data": None, "error": "Role already exists"}

        role = Role(name=role_name)

        db.add(role)
        db.commit()
        db.refresh(role)

        return {
            "data": {
                "id": role.id,
                "name": role.name.upper()
            },
            "error": None
        }

    # =====================
    # GET ALL ROLES
    # =====================
    @staticmethod
    def get_roles(db):

        roles = db.query(Role).all()

        return {
            "data": [
                {
                    "id": r.id,
                    "name": r.name.upper()
                }
                for r in roles
            ],
            "error": None
        }

    # =====================
    # GET ROLE BY ID
    # =====================
    @staticmethod
    def get_role_by_id(db, role_id):

        role = db.query(Role).filter(
            Role.id == role_id
        ).first()

        if not role:
            return {"data": None, "error": "Role not found"}

        return {
            "data": {
                "id": role.id,
                "name": role.name.upper()
            },
            "error": None
        }

    # =====================
    # UPDATE ROLE
    # =====================
    @staticmethod
    def update_role(db, role_id, data):

        role = db.query(Role).filter(
            Role.id == role_id
        ).first()

        if not role:
            return {"data": None, "error": "Role not found"}

        if "name" in data:

            new_name = RoleService.normalize(data["name"])

            existing = db.query(Role).filter(
                Role.name == new_name
            ).first()

            if existing and existing.id != role.id:
                return {"data": None, "error": "Role already exists"}

            role.name = new_name

        db.commit()
        db.refresh(role)

        return {
            "data": {
                "id": role.id,
                "name": role.name.upper()
            },
            "error": None
        }

    # =====================
    # DELETE ROLE
    # =====================
    @staticmethod
    def delete_role(db, role_id):

        role = db.query(Role).filter(
            Role.id == role_id
        ).first()

        if not role:
            return {"data": None, "error": "Role not found"}

        db.delete(role)
        db.commit()

        return {
            "data": {
                "message": "Role deleted successfully"
            },
            "error": None
        }

    # =====================
    # CHECK ROLE EXISTS
    # =====================
    @staticmethod
    def is_valid(db, role: str) -> bool:

        if not role:
            return False

        role = RoleService.normalize(role)

        existing = db.query(Role).filter(
            Role.name == role
        ).first()

        return existing is not None

    # =====================
    # GET ROLE NAMES
    # =====================
    @staticmethod
    def get_role_names(db):

        roles = db.query(Role).all()

        return [
            role.name.upper()
            for role in roles
        ]