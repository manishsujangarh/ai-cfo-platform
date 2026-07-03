from sqlalchemy import select
from sqlalchemy.orm import Session

from app.organization_members.model import OrganizationMember

def get_membership(
    db: Session,
    organization_id: int,
    user_id: int,
):
    return (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == user_id,
        )
        .first()
    )

def create_member(
    db: Session,
    organization_id: int,
    user_id: int,
    role: str,
):
    member = OrganizationMember(
        organization_id=organization_id,
        user_id=user_id,
        role=role,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member

def get_by_user_id(
    db: Session,
    user_id: int,
) -> OrganizationMember | None:
    statement = (
        select(OrganizationMember)
        .where(
            OrganizationMember.user_id == user_id
        )
    )

    return db.scalar(statement)