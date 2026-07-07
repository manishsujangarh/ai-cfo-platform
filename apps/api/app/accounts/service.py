from sqlalchemy.orm import Session

from app.accounts.repository import (
    create_account,
    get_by_id,
    list_all,
)


def create(
    db: Session,
    organization_id: int,
    code: str,
    name: str,
    type: str,
    subtype: str | None,
):
    return create_account(
        db=db,
        organization_id=organization_id,
        code=code,
        name=name,
        type=type,
        subtype=subtype,
    )


def get(
    db: Session,
    account_id: int,
):
    return get_by_id(db, account_id)


def list_all_accounts(
    db: Session,
):
    return list_all(db)