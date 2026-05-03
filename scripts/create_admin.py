from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role
from werkzeug.security import generate_password_hash


def create_admin():
    db = SessionLocal()

    try:
        # 1. vérifier ou créer rôle ADMIN
        role = db.query(Role).filter(Role.name == "ADMIN").first()

        if not role:
            role = Role(name="ADMIN")
            db.add(role)
            db.commit()
            db.refresh(role)

        # 2. vérifier si admin existe déjà
        admin = db.query(User).filter(User.email == "badreddine@yahoo.fr").first()

        if admin:
            print("Admin already exists")
            return

        # 3. créer admin
        admin = User(
            email="badreddine@yahoo.fr",
            password=generate_password_hash("Setif_19000"),
            role_id=role.id
        )

        db.add(admin)
        db.commit()

        print("Admin created successfully")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()