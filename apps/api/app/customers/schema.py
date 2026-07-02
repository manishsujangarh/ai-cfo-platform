from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    organization_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class CustomerResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True