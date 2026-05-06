from werkzeug.security import generate_password_hash
from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role


def create_admin():
    db = SessionLocal()

    try:
        # 🔥 valeurs FIXES (pas de variable externe = zéro bug)
        username = "badreddine"
        email = "badreddine@yahoo.fr"
        password = "Setif_19000"

        # 1. récupérer rôle ADMIN
        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()

        if not admin_role:
            print("❌ Role ADMIN introuvable")
            return

        # 2. vérifier si user existe déjà
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            print("⚠️ User already exists")
            return

        # 3. créer user admin
        # 3. créer user admin
        print("USERNAME BEFORE INSERT:", repr(username))
        print("EMAIL BEFORE INSERT:", repr(email))

        admin_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role_id=admin_role.id
        )
        admin_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role_id=admin_role.id
        )

        db.add(admin_user)
        db.commit()

        print("✅ Admin created successfully")

    except Exception as e:
        db.rollback()
        print("❌ ERROR:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()

# from app.core.db import SessionLocal
# from app.modules.users.model import User
# from app.modules.roles.model import Role
# from werkzeug.security import generate_password_hash
#
#
# def create_admin():
#     db = SessionLocal()
#
#     try:
#         # 1. vérifier ou créer rôle ADMIN
#         role = db.query(Role).filter(Role.name == "ADMIN").first()
#
#         if not role:
#             role = Role(name="ADMIN")
#             db.add(role)
#             db.commit()
#             db.refresh(role)
#
#         # 2. vérifier si admin existe déjà
#         admin = db.query(User).filter(User.email == "badreddine@yahoo.fr").first()
#
#         if admin:
#             print("Admin already exists")
#             return
#
#         # 3. créer admin
#         admin = User(
#             email="badreddine@yahoo.fr",
#             password=generate_password_hash("Setif_19000"),
#             role_id=role.id
#         )
#
#         db.add(admin)
#         db.commit()
#
#         print("Admin created successfully")
#
#     finally:
#         db.close()
#
#
# if __name__ == "__main__":
#     create_admin()
