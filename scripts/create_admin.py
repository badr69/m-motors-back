from werkzeug.security import generate_password_hash
from app.core.db import SessionLocal
from app.modules.users.model import User
from app.modules.roles.model import Role


def create_admin():
    db = SessionLocal()

    try:
        # =========================
        # CREATE ADMIN ROLE
        # =========================
        admin_role = db.query(Role).filter_by(name="ADMIN").first()

        if not admin_role:
            admin_role = Role(name="ADMIN")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

            print("✅ ADMIN role created")

        # =========================
        # ADMIN USER DATA
        # =========================
        username = "badreddine"
        email = "badreddine@yahoo.fr"
        password = "Setif_19000"

        # =========================
        # CHECK EXISTING USER
        # =========================
        existing_user = db.query(User).filter_by(email=email).first()

        if existing_user:
            print("⚠️ Admin already exists")
            return

        # =========================
        # CREATE ADMIN USER
        # =========================
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