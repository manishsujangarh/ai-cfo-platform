from sqlalchemy.orm import Session

from app.organization_members.model import OrganizationMember
from app.organizations.model import Organization


def create_organization(
    db: Session,
    name: str,
    slug: str,
):
    organization = Organization(
        name=name,
        slug=slug,
    )

    db.add(organization)
    db.commit()
    db.refresh(organization)

    return organization


def list_organizations(
    db: Session,
    user_id: int,
):
    return (
        db.query(Organization)
        .join(
            OrganizationMember,
            Organization.id == OrganizationMember.organization_id,
        )
        .filter(
            OrganizationMember.user_id == user_id,
        )
        .all()
    )


def get_organization(
    db: Session,
    organization_id: int,
):
    return (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )