from fastapi import FastAPI

from app.core.config import settings
from app.repositories.health_repository import get_db_version
from app.users.api import router as users_router
from app.auth.api import router as auth_router
from app.organizations.api import router as organizations_router
from app.customers.api import router as customers_router
from app.vendors.api import router as vendors_router
from app.journal_entries.api import router as journal_entries_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(organizations_router)
app.include_router(customers_router)
app.include_router(vendors_router)
app.include_router(journal_entries_router)


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "database": get_db_version(),
    }