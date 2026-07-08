from sqlalchemy.orm import Session
from app.accounts.default_accounts import DEFAULT_ACCOUNTS
from app.accounts.model import Account
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


def create_default_accounts(
    db: Session,
    organization_id: int,
):
    accounts = []

    for item in DEFAULT_ACCOUNTS:
        account = Account(
            organization_id=organization_id,
            code=item["code"],
            name=item["name"],
            type=item["type"],
            subtype=item["subtype"],
        )

        db.add(account)
        accounts.append(account)

    db.commit()

    return accounts