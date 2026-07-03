from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.vendors.model import Vendor



def create_vendor(db: Session, organization_id: int, name: str, email: str | None, phone: str | None, address: str | None, gst_number: str | None):
    vendor = Vendor(
        organization_id=organization_id,
        name=name,
        email=email,
        phone=phone,
        address=address,
        gst_number=gst_number,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),

    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor 


def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()


def get_vendors(db: Session):
    return db.query(Vendor).all()


def count_vendors(
    db: Session,
    organization_id: int,
) -> int:
    statement = (
        select(func.count(Vendor.id))
        .where(
            Vendor.organization_id == organization_id
        )
    )

    return db.scalar(statement) or 0