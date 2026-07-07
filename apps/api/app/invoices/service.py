from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.customers.repository import get_by_id as get_customer_by_id

from app.invoices.calculator import calculate_invoice

from app.invoices.model import Invoice

from app.accounts.posting import post_invoice
from app.invoices.repository import (
    create as repository_create,
    delete as repository_delete,
    get_by_id,
    get_by_invoice_number,
    list_all as repository_list_all,
    update as repository_update,
)

from app.invoices.schema import (
    InvoiceCreate,
    InvoiceUpdate,
)


def create(
    db: Session,
    request: InvoiceCreate,
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

    existing = get_by_invoice_number(
        db,
        request.organization_id,
        request.invoice_number,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Invoice number already exists",
        )

    items, subtotal, discount, tax, total = calculate_invoice(
        request.items,
    )

    invoice = Invoice(
        organization_id=request.organization_id,
        customer_id=request.customer_id,
        invoice_number=request.invoice_number,
        invoice_date=request.invoice_date,
        due_date=request.due_date,
        notes=request.notes,
        status="draft",
        subtotal=subtotal,
        discount=discount,
        tax=tax,
        total=total,
    )

    invoice.items = items

    invoice = repository_create(
    db,
    invoice,
    )

    post_invoice(
    db,
    invoice,
    )
    return invoice


def get(
    db: Session,
    invoice_id: int,
):
    return get_by_id(
        db,
        invoice_id,
    )


def list_all(
    db: Session,
):
    return repository_list_all(
        db,
    )


def update(
    db: Session,
    invoice_id: int,
    request: InvoiceUpdate,
):
    invoice = get_by_id(
        db,
        invoice_id,
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found",
        )

    items, subtotal, discount, tax, total = calculate_invoice(
        request.items,
    )

    invoice.invoice_date = request.invoice_date
    invoice.due_date = request.due_date
    invoice.notes = request.notes

    invoice.items.clear()
    invoice.items.extend(items)

    invoice.subtotal = subtotal
    invoice.discount = discount
    invoice.tax = tax
    invoice.total = total

    return repository_update(
        db,
        invoice,
    )


def delete(
    db: Session,
    invoice_id: int,
):
    invoice = get_by_id(
        db,
        invoice_id,
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found",
        )

    repository_delete(
        db,
        invoice,
    )