from sqlalchemy import func
from sqlalchemy.orm import Session

from app.customers.model import Customer


def create_customer(db: Session, organization_id: int, name: str, email: str | None, phone: str | None, address: str | None):
    customer = Customer(
        organization_id=organization_id,
        name=name,
        email=email,
        phone=phone,
        address=address
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer 


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customers(db: Session):
    return db.query(Customer).all()



def count_customers(
    db: Session,
    organization_id: int,
) -> int:
    """
    Return the total number of customers for an organization.
    """

    return (
        db.query(func.count(Customer.id))
        .filter(
            Customer.organization_id == organization_id
        )
        .scalar()
        or 0
    )