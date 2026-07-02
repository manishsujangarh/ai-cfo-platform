from sqlalchemy.orm import Session

# Import the password hashing utility you created earlier
from app.auth.security import hash_password
from app.users.repository import (
    create_user,
    get_user,
    get_users,
)


def create_new_user(db: Session, email: str, full_name: str | None, password: str):
    # Hash the plaintext password securely before sending it to the database
    hashed_password = hash_password(password)
    
    # Pass the hash down to the repository layer
    return create_user(db, email, full_name, hashed_password)


def fetch_user(db: Session, user_id: int):
    return get_user(db, user_id)


def fetch_users(db: Session):
    return get_users(db)