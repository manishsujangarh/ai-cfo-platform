from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    id: int
    organization_id: int
    code: str
    name: str
    type: str
    subtype: str | None = None


class AccountResponse(BaseModel):
    id: int
    organization_id: int
    code: str
    name: str
    type: str
    subtype: str | None = None


    class Config:
        from_attributes = True