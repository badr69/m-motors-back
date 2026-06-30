import os
from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import hash_password


def create_admin():
    db = SessionLocal()

    try:
        # 👉 Admin de démonstration (tes identifiants)
        admin_username = "badreddine"
        admin_email = "badreddine@yahoo.fr"
        admin_password = "Studi$26?"

        role = db.query(Role).filter(Role.name == "ADMIN").first()

        if not role:
            role = Role(name="ADMIN")
            db.add(role)
            db.commit()
            db.refresh(role)

        admin = db.query(User).filter(User.email == admin_email).first()

        if admin:
            print("Admin already exists")
            return

        admin = User(
            username=admin_username,
            email=admin_email,
            password_hash=hash_password(admin_password),
            role_id=role.id,
            is_active=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin created successfully")

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()





