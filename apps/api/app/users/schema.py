from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    password: str  # <--- Added so FastAPI expects it on signup


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    # ❌ Removed password field to protect sensitive hash data

    class Config:
        from_attributes = True