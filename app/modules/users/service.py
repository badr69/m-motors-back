from sqlalchemy.orm import joinedload
from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import hash_password


class UserService:

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    def create_user(data):

        db = SessionLocal()

        try:
            role_id = data.get("role_id")

            if not role_id:
                return None, "Role required"

            role = (
                db.query(Role)
                .filter(Role.id == role_id)
                .first()
            )

            if not role:
                return None, "Role not found"

            if role.name.upper() == "ADMIN":
                return None, "Cannot create ADMIN user"

            user = User(
                username=data.get("username"),
                email=data.get("email"),
                password_hash=hash_password(data.get("password")),
                phone=data.get("phone"),
                address=data.get("address"),
                role_id=role_id
            )

            db.add(user)
            db.commit()

            created_user = (
                db.query(User)
                .options(joinedload(User.role))
                .filter(User.id == user.id)
                .first()
            )

            return created_user, None

        except Exception as e:
            db.rollback()
            print("[USER CREATE ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # GET ALL USERS
    # =====================
    @staticmethod
    def get_users():

        db = SessionLocal()

        try:
            users = (
                db.query(User)
                .options(joinedload(User.role))
                .all()
            )

            return users, None

        except Exception as e:
            print("[USER GET ALL ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # GET USER BY ID
    # =====================
    @staticmethod
    def get_user_by_id(user_id):

        db = SessionLocal()

        try:
            user = (
                db.query(User)
                .options(joinedload(User.role))
                .filter(User.id == user_id)
                .first()
            )

            if not user:
                return None, "User not found"

            return user, None

        except Exception as e:
            print("[USER GET ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update_user(user_id, data, current_user):

        db = SessionLocal()

        try:
            user = (
                db.query(User)
                .options(joinedload(User.role))
                .filter(User.id == user_id)
                .first()
            )

            if not user:
                return None, "User not found"

            current_id = int(current_user.get("user_id"))
            current_role = (current_user.get("role") or "").upper()

            if user.role and user.role.name.upper() == "ADMIN":
                return None, "Cannot modify ADMIN user"

            if current_role != "ADMIN" and current_id != user_id:
                return None, "Forbidden"

            if "username" in data:
                user.username = data["username"]

            if "email" in data:
                user.email = data["email"]

            if "phone" in data:
                user.phone = data["phone"]

            if "address" in data:
                user.address = data["address"]

            if data.get("password"):
                user.password_hash = hash_password(data["password"])

            if data.get("role_id") and current_role == "ADMIN":

                new_role = (
                    db.query(Role)
                    .filter(Role.id == data["role_id"])
                    .first()
                )

                if not new_role:
                    return None, "Role not found"

                if new_role.name.upper() == "ADMIN":
                    return None, "Cannot assign ADMIN role"

                user.role_id = new_role.id

            db.commit()

            updated_user = (
                db.query(User)
                .options(joinedload(User.role))
                .filter(User.id == user.id)
                .first()
            )

            return updated_user, None

        except Exception as e:
            db.rollback()
            print("[USER UPDATE ERROR]", str(e))
            return None, "Server error"

        finally:
            db.close()

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete_user(user_id, current_user):

        db = SessionLocal()

        try:
            user = (
                db.query(User)
                .options(joinedload(User.role))
                .filter(User.id == user_id)
                .first()
            )

            if not user:
                return False, "User not found"

            try:
                current_id = int(current_user.get("user_id"))
            except:
                return False, "Invalid token user_id"

            current_role = (current_user.get("role") or "").upper()

            if user.role and user.role.name.upper() == "ADMIN":
                return False, "Cannot delete ADMIN user"

            if current_role != "ADMIN" and current_id != user_id:
                return False, "Forbidden"

            db.delete(user)
            db.commit()

            return True, None

        except Exception as e:
            db.rollback()
            print("[USER DELETE ERROR]", str(e))
            return False, "Server error"

        finally:
            db.close()