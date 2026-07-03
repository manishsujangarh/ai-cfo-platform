from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.customers.repository import get_by_id as get_customer_by_id
from app.invoices.repository import get_by_id as get_invoice_by_id

from app.payments.model import Payment

from app.payments.repository import (
    create as repository_create,
    delete as repository_delete,
    get_by_id,
    get_by_payment_number,
    list_all as repository_list_all,
    update as repository_update,
)

from app.payments.schema import (
    PaymentCreate,
    PaymentUpdate,
)


def create(
    db: Session,
    request: PaymentCreate,
):
    customer = get_customer_by_id(
        db,
        request.customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    if request.invoice_id is not None:
        invoice = get_invoice_by_id(
            db,
            request.invoice_id,
        )

        if invoice is None:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found",
            )

    existing = get_by_payment_number(
        db,
        request.payment_number,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Payment number already exists",
        )

    payment = Payment(
        organization_id=request.organization_id,
        customer_id=request.customer_id,
        invoice_id=request.invoice_id,
        payment_number=request.payment_number,
        payment_date=request.payment_date,
        amount=request.amount,
        payment_method=request.payment_method,
        reference=request.reference,
        notes=request.notes,
    )

    return repository_create(
        db,
        payment,
    )


def get(
    db: Session,
    payment_id: int,
):
    return get_by_id(
        db,
        payment_id,
    )


def list_all(
    db: Session,
):
    return repository_list_all(
        db,
    )


def update(
    db: Session,
    payment_id: int,
    request: PaymentUpdate,
):
    payment = get_by_id(
        db,
        payment_id,
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    payment.payment_date = request.payment_date
    payment.amount = request.amount
    payment.payment_method = request.payment_method
    payment.reference = request.reference
    payment.notes = request.notes
    payment.status = request.status

    return repository_update(
        db,
        payment,
    )


def delete(
    db: Session,
    payment_id: int,
):
    payment = get_by_id(
        db,
        payment_id,
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    repository_delete(
        db,
        payment,
    )