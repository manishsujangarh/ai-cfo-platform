from sqlalchemy.orm import Session

from app.users.model import User


def create_user(db: Session, email: str, full_name: str | None):
    user = User(email=email, full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()