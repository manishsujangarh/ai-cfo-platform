from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.payments.schema import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
)

from app.payments.service import (
    create,
    get,
    list_all,
    update,
    delete,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentResponse,
)
def create_payment(
    request: PaymentCreate,
    db: Session = Depends(get_db),
):
    return create(
        db,
        request,
    )


@router.get(
    "",
    response_model=list[PaymentResponse],
)
def get_payments(
    db: Session = Depends(get_db),
):
    return list_all(
        db,
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    payment = get(
        db,
        payment_id,
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    return payment


@router.put(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def update_payment(
    payment_id: int,
    request: PaymentUpdate,
    db: Session = Depends(get_db),
):
    return update(
        db,
        payment_id,
        request,
    )


@router.delete(
    "/{payment_id}",
)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    delete(
        db,
        payment_id,
    )

    return {
        "message": "Payment deleted successfully",
    }