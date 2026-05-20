import os
from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import hash_password
from dotenv import load_dotenv

load_dotenv()


def create_admin():
    db = SessionLocal()

    try:
        admin_email = os.getenv("ADMIN_EMAIL", "").strip()
        admin_username = os.getenv("ADMIN_USERNAME", "").strip()
        admin_password = os.getenv("ADMIN_PASSWORD", "").strip()

        if not all([admin_email, admin_username, admin_password]):
            print("Missing ENV variables")
            return

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