from sqlalchemy.orm import Session

from app.users.repository import (
    create_user,
    get_user,
    get_users,
)


def create_new_user(db: Session, email: str, full_name: str | None):
    # future place for validation, fraud checks, AI scoring, etc.
    return create_user(db, email, full_name)


def fetch_user(db: Session, user_id: int):
    return get_user(db, user_id)


def fetch_users(db: Session):
    return get_users(db)