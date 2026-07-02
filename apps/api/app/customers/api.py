from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.customers.schema import CustomerCreate, CustomerResponse
from app.customers.service import (
    create_new_customer,
    fetch_customer,
    fetch_customers,
)

from app.auth.dependency import get_current_user
from app.users.model import User

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Pass the plaintext password from the schema to your service layer
    return create_new_customer(db, customer.organization_id, customer.name, customer.email, customer.phone, customer.address)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return fetch_customer(db, customer_id)


@router.get("/", response_model=list[CustomerResponse])
def list_customers(db: Session = Depends(get_db)):
    return fetch_customers(db)

