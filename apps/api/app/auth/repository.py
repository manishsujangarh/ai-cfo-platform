from sqlalchemy import select

from app.db.session import SessionLocal
from app.users.model import User


def get_user_by_email(email: str) -> User | None:
    with SessionLocal() as session:
        statement = select(User).where(User.email == email)
        return session.scalar(statement)