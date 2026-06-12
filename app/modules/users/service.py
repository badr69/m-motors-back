from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import hash_password
from app.core.logger import setup_logger

logger = setup_logger("user-service")


# =====================
# HELPER
# =====================
def get_role_name(user):
    return user.role.name.upper() if user.role else "CLIENT"


class UserService:

    # =====================
    # CREATE USER
    # =====================
    @staticmethod
    def create_user(db, data):

        logger.info(f"Creating user: {data.get('email')}")

        role_id = data.get("role_id")

        role = db.query(Role).filter(Role.id == role_id).first()

        if not role:
            return {"data": None, "error": "Role not found"}

        if db.query(User).filter(User.email == data.get("email")).first():
            return {"data": None, "error": "Email already exists"}

        if db.query(User).filter(User.username == data.get("username")).first():
            return {"data": None, "error": "Username already exists"}

        user = User(
            username=data.get("username"),
            email=data.get("email"),
            password_hash=hash_password(data.get("password")),
            phone=data.get("phone"),
            address=data.get("address"),
            role_id=role.id,
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role": get_role_name(user)
            },
            "error": None
        }

    # =====================
    # GET ALL USERS
    # =====================
    @staticmethod
    def get_users(db):

        users = db.query(User).all()

        return {
            "data": [
                {
                    "id": u.id,
                    "username": u.username,
                    "email": u.email,
                    "phone": u.phone,
                    "address": u.address,
                    "role": get_role_name(u),
                    "is_active": u.is_active
                }
                for u in users
            ],
            "error": None
        }

    # =====================
    # GET USER BY ID
    # =====================
    @staticmethod
    def get_user_by_id(db, current_user, user_id):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {"data": None, "error": "User not found"}

        role = (current_user or {}).get("role")
        current_id = (current_user or {}).get("user_id")

        is_admin = role == "ADMIN"
        is_owner = current_id == user_id

        if not is_admin and not is_owner:
            return {"data": None, "error": "Forbidden"}

        return {
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role": get_role_name(user),
                "is_active": user.is_active
            },
            "error": None
        }

    # =====================
    # UPDATE USER
    # =====================
    @staticmethod
    def update_user(db, user_id, data):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {"data": None, "error": "User not found"}

        if "email" in data:
            existing = db.query(User).filter(User.email == data["email"]).first()
            if existing and existing.id != user.id:
                return {"data": None, "error": "Email already exists"}

        for field in ["username", "email", "phone", "address"]:
            if field in data:
                setattr(user, field, data[field])

        db.commit()
        db.refresh(user)

        return {
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role": get_role_name(user),
                "is_active": user.is_active
            },
            "error": None
        }

    # =====================
    # DELETE USER
    # =====================
    @staticmethod
    def delete_user(db, user_id):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {"data": None, "error": "User not found"}

        db.delete(user)
        db.commit()

        return {
            "data": {"message": "User deleted successfully"},
            "error": None
        }

    # =====================
    # GET ME
    # =====================
    @staticmethod
    def get_me(db, user_id):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {"data": None, "error": "User not found"}

        return {
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role": get_role_name(user)
            },
            "error": None
        }

    # =====================
    # UPDATE ME
    # =====================
    @staticmethod
    def update_me(db, user_id, data):

        return UserService.update_user(db, user_id, data)

    # =====================
    # DELETE ME
    # =====================
    @staticmethod
    def delete_me(db, user_id):

        return UserService.delete_user(db, user_id)













# from app.modules.users.model import User
# from app.modules.roles.model import Role
# from app.core.security.password import hash_password
# from app.core.logger import setup_logger
#
# logger = setup_logger("user-service")
#
#
# # =====================
# # HELPER
# # =====================
# def get_role_name(user):
#     return user.role.name.upper() if user.role else "CLIENT"
#
#
# class UserService:
#
#     # =====================
#     # CREATE USER
#     # =====================
#     @staticmethod
#     def create_user(db, data):
#
#         logger.info(f"Creating user: {data.get('email')}")
#
#         # 🔥 DEBUG
#         print("🔥 [DEBUG] CREATE USER DATA:", data)
#
#         # =====================
#         # ROLE ID EXTRACTION
#         # =====================
#         role_id = data.get("role_id")
#         print("🔥 [DEBUG] ROLE_ID:", role_id)
#
#         # =====================
#         # ROLE CHECK
#         # =====================
#         role = db.query(Role).filter(Role.id == role_id).first()
#
#         if not role:
#             print("❌ ROLE NOT FOUND FOR ID:", role_id)
#             logger.warning("Role not found during user creation")
#             return {"data": None, "error": "Role not found"}
#
#         # =====================
#         # EMAIL CHECK
#         # =====================
#         if db.query(User).filter(User.email == data.get("email")).first():
#             logger.warning(f"Email already exists: {data.get('email')}")
#             return {"data": None, "error": "Email already exists"}
#
#         # =====================
#         # CREATE USER
#         # =====================
#         user = User(
#             username=data.get("username"),
#             email=data.get("email"),
#             password_hash=hash_password(data.get("password")),
#             phone=data.get("phone"),
#             address=data.get("address"),
#             role_id=role.id,
#             is_active=True
#         )
#
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#
#         logger.info(f"User created successfully: {user.email}")
#
#         return {
#             "data": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "phone": user.phone,
#                 "address": user.address,
#                 "role": get_role_name(user)
#             },
#             "error": None
#         }
#
#     # =====================
#     # GET ALL USERS
#     # =====================
#     @staticmethod
#     def get_users(db):
#
#         users = db.query(User).all()
#
#         return {
#             "data": [
#                 {
#                     "id": u.id,
#                     "username": u.username,
#                     "email": u.email,
#                     "phone": u.phone,
#                     "address": u.address,
#                     "role": get_role_name(u),
#                     "is_active": u.is_active
#                 }
#                 for u in users
#             ],
#             "error": None
#         }
#
#     # =====================
#     # GET USER BY ID
#     # =====================
#     @staticmethod
#     def get_user_by_id(db, current_user, user_id):
#
#         user = db.query(User).filter(User.id == user_id).first()
#
#         if not user:
#             return {"data": None, "error": "User not found"}
#
#         role = (current_user or {}).get("role")
#         current_id = (current_user or {}).get("user_id")
#
#         is_admin = role == "ADMIN"
#         is_owner = current_id == user_id
#
#         if not is_admin and not is_owner:
#             return {"data": None, "error": "Forbidden"}
#
#         return {
#             "data": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "phone": user.phone,
#                 "address": user.address,
#                 "role": get_role_name(user),
#                 "is_active": user.is_active
#             },
#             "error": None
#         }
#     # =====================
#     # UPDATE USER
#     # =====================
#     @staticmethod
#     def update_user(db, user_id, data):
#
#         user = db.query(User).filter(User.id == user_id).first()
#
#         if not user:
#             return {"data": None, "error": "User not found"}
#
#         if "email" in data:
#             existing = db.query(User).filter(User.email == data["email"]).first()
#             if existing and existing.id != user.id:
#                 return {"data": None, "error": "Email already exists"}
#
#         for field in ["username", "email", "phone", "address"]:
#             if field in data:
#                 setattr(user, field, data[field])
#
#         db.commit()
#         db.refresh(user)
#
#         return {
#             "data": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "phone": user.phone,
#                 "address": user.address,
#                 "role": get_role_name(user),
#                 "is_active": user.is_active
#             },
#             "error": None
#         }
#
#     # =====================
#     # DELETE USER
#     # =====================
#     @staticmethod
#     def delete_user(db, user_id):
#
#         user = db.query(User).filter(User.id == user_id).first()
#
#         if not user:
#             return {"data": None, "error": "User not found"}
#
#         db.delete(user)
#         db.commit()
#
#         return {
#             "data": {"message": "User deleted successfully"},
#             "error": None
#         }
#
#     # =====================
#     # GET ME
#     # =====================
#     @staticmethod
#     def get_me(db, current_user):
#
#         if not current_user:
#             return {"data": None, "error": "Unauthorized"}
#
#         user_id = current_user.get("user_id")
#
#         if not user_id:
#             return {"data": None, "error": "Invalid token payload"}
#
#         user = db.query(User).filter(User.id == user_id).first()
#
#         if not user:
#             return {"data": None, "error": "User not found"}
#
#         return {
#             "data": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "phone": user.phone,
#                 "address": user.address,
#                 "role": get_role_name(user)
#             },
#             "error": None
#         }
#     # =====================
#     # UPDATE ME
#     # =====================
#     @staticmethod
#     def update_me(db, current_user, data):
#
#         return UserService.update_user(db, current_user.get("user_id"), data)
#
#     # =====================
#     # DELETE ME
#     # =====================
#     @staticmethod
#     def delete_me(db, current_user):
#
#         return UserService.delete_user(db, current_user.get("user_id"))