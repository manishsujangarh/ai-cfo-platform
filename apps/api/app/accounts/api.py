from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.accounts.schema import AccountCreate, AccountResponse
from app.accounts.service import (
    create,
    get,
    list_all_accounts,
)

from app.auth.dependency import get_current_user
from app.users.model import User

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    # Pass the plaintext password from the schema to your service layer
    return create(db, account.organization_id, account.code, account.name, account.type, account.subtype)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return get(db, account_id)


@router.get("/", response_model=list[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    return list_all_accounts(db)

