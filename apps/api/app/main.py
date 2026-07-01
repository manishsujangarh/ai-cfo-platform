from fastapi import FastAPI

from app.core.config import settings
from app.repositories.health_repository import get_db_version

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "database": get_db_version(),
    }