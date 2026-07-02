import re

from sqlalchemy.orm import Session


from app.organizations.repository import (
    create_organization,
    get_organization,
    list_organizations,
)

from app.organization_members.repository import create_member

def slugify(text: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "-",
        text.lower(),
    ).strip("-")


def create(
    db: Session,
    name: str,
    user_id: int,
):
    slug = slugify(name)

    organization = create_organization(
        db=db,
        name=name,
        slug=slug,
    )

    create_member(
        db=db,
        organization_id=organization.id,
        user_id=user_id,
        role="OWNER",
    )

    return organization

def list_all(
    db,
    user_id: int,
):
    return list_organizations(
        db,
        user_id,
    )


def get_by_id(
    db: Session,
    organization_id: int,
):
    return get_organization(
        db,
        organization_id,
    )