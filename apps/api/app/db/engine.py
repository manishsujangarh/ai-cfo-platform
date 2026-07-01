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

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)