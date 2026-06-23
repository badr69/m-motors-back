from app.modules import Role


def seed_roles(db):
    roles = ["ADMIN", "CLIENT"]

    for role_name in roles:
        exists = db.query(Role).filter_by(name=role_name).first()
        if not exists:
            db.add(Role(name=role_name))

    db.commit()