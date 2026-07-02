from app.auth.repository import get_user_by_email
from app.auth.security import (
    create_access_token,
    verify_password,
)


def login(email: str, password: str):
    user = get_user_by_email(email)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token(user.email)

    return {
        "access_token": token,
        "token_type": "bearer",
    }