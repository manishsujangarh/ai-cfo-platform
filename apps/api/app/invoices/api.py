from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.invoices.schema import (
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceResponse,
)

from app.invoices.service import (
    create,
    get,
    list_all,
    update,
    delete,
)

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
)


@router.post(
    "",
    response_model=InvoiceResponse,
)
def create_invoice(
    request: InvoiceCreate,
    db: Session = Depends(get_db),
):
    return create(
        db,
        request,
    )


@router.get(
    "",
    response_model=list[InvoiceResponse],
)
def get_invoices(
    db: Session = Depends(get_db),
):
    return list_all(
        db,
    )


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse,
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    invoice = get(
        db,
        invoice_id,
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found",
        )

    return invoice


@router.put(
    "/{invoice_id}",
    response_model=InvoiceResponse,
)
def update_invoice(
    invoice_id: int,
    request: InvoiceUpdate,
    db: Session = Depends(get_db),
):
    return update(
        db,
        invoice_id,
        request,
    )


@router.delete(
    "/{invoice_id}",
)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    delete(
        db,
        invoice_id,
    )

    return {
        "message": "Invoice deleted successfully",
    }