from sqlalchemy.orm import Session

# Import the password hashing utility you created earlier
from app.vendors.repository import (
    create_vendor,
    get_vendor,
    get_vendors,
)


def create_new_vendor(db: Session, organization_id: int, name: str, email: str | None, phone: str | None, address: str | None, gst_number: str | None):

    return create_vendor(db, organization_id, name, email, phone, address, gst_number)


def fetch_vendor(db: Session, vendor_id: int):
    return get_vendor(db, vendor_id)


def fetch_vendors(db: Session):
    return get_vendors(db)