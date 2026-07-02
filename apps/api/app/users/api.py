from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.users.schema import UserCreate, UserResponse
from app.users.service import (
    create_new_user,
    fetch_user,
    fetch_users,
)

from app.auth.dependency import get_current_user
from app.users.model import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Pass the plaintext password from the schema to your service layer
    return create_new_user(db, user.email, user.full_name, user.password)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return fetch_user(db, user_id)


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return fetch_users(db)

