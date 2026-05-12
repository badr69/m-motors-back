from sqlalchemy.orm import Session
from app.modules.users.model import User


class UserService:

    # CREATE
    @staticmethod
    def create_user(db: Session, user_data: dict):
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # READ ALL
    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    # READ BY ID
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # READ BY EMAIL
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    # READ BY USERNAME
    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    # UPDATE
    @staticmethod
    def update_user(db: Session, user: User, data: dict):
        print(data)
        for key, value in data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    # DELETE
    @staticmethod
    def delete_user(db: Session, user: User):
        db.delete(user)
        db.commit()