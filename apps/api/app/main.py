from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
    }
@app.get("/api/v1")
def root():
    return {
        "message": "Welcome to AI CFO API v1"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

