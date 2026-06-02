from app.modules.roles.model import Role


def seed_roles(db):
    if db.query(Role).count() == 0:
        db.add_all([
            Role(name="ADMIN"),
            Role(name="CLIENT")
        ])
        db.commit()