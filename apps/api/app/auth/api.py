from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schema import TokenResponse
from app.auth.service import login

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    token = login(
        form_data.username,  # email goes here
        form_data.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return token