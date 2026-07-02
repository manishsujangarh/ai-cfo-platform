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