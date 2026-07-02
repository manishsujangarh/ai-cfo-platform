from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependency import get_current_user
from app.db.session import get_db
from app.organizations.schema import (
    OrganizationCreate,
    OrganizationResponse,
)
from app.organizations.service import (
    create,
    get_by_id,
    list_all,
)

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
)
def create_org(
    request: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create(
        db=db,
        name=request.name,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[OrganizationResponse],
)
def get_orgs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_all(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_org(
    organization_id: int,
    db: Session = Depends(get_db),
):
    organization = get_by_id(
        db,
        organization_id,
    )

    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    return organization