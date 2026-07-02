from sqlalchemy.orm import Session

# Import the password hashing utility you created earlier
from app.auth.security import hash_password
from app.customers.repository import (
    create_customer,
    get_customer,
    get_customers,
)


def create_new_customer(db: Session, organization_id: int, name: str, email: str | None, phone: str | None, address: str | None):

    return create_customer(db, organization_id, name, email, phone, address)


def fetch_customer(db: Session, customer_id: int):
    return get_customer(db, customer_id)


def fetch_customers(db: Session):
    return get_customers(db)