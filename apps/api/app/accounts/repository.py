from sqlalchemy.orm import Session

from datetime import datetime
from app.accounts.model import Account


def create_account(db: Session, organization_id: int, code: str, name: str, type: str, subtype: str | None):
    account = Account(
        organization_id=organization_id,
        code=code,
        name=name,
        type=type,
        subtype=subtype,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_by_code(
    db: Session,
    organization_id: int,
    code: str,
) -> Account | None:
    return (
        db.query(Account)
        .filter(
            Account.organization_id == organization_id,
            Account.code == code,
        )
        .first()
    )

def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def get_accounts(db: Session):
    return db.query(Account).all()