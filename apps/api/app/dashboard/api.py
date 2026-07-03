from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from  app.db.session import get_db 
from app.dashboard.schemas import DashboardSummary
from app.dashboard.service import get_dashboard_summary

from app.auth.dependency import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_dashboard_summary(
        db=db,
        organization_id=current_user.organization_id,
    )