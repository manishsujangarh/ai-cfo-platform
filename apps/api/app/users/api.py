from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.users.schema import UserCreate, UserResponse
from app.users.service import (
    create_new_user,
    fetch_user,
    fetch_users,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(db, user.email, user.full_name)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return fetch_user(db, user_id)


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return fetch_users(db)