from pydantic import BaseModel, EmailStr


class VendorCreate(BaseModel):
    organization_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    gst_number: str | None = None


class VendorResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    gst_number: str | None = None

    class Config:
        from_attributes = True