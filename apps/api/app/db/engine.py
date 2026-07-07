from sqlalchemy import create_engine
from app.core.config import settings

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.database_user}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

print("DATABASE_USER =", settings.database_user)
print("DATABASE_NAME =", settings.database_name)
print("DATABASE_HOST =", settings.database_host)
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)