from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.vendors.schema import VendorCreate, VendorResponse
from app.vendors.service import (
    create_new_vendor,
    fetch_vendor,
    fetch_vendors,
)

from app.auth.dependency import get_current_user
from app.users.model import User

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/", response_model=VendorResponse)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    # Pass the plaintext password from the schema to your service layer
    return create_new_vendor(db, vendor.organization_id, vendor.name, vendor.email, vendor.phone, vendor.address, vendor.gst_number)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    return fetch_vendor(db, vendor_id)


@router.get("/", response_model=list[VendorResponse])
def list_vendors(db: Session = Depends(get_db)):
    return fetch_vendors(db)

