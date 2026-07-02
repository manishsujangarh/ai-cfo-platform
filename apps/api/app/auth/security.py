from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )