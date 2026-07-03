from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.payments.model import (
    PaymentMethod,
    PaymentStatus,
)


class PaymentCreate(BaseModel):
    organization_id: int

    customer_id: int

    invoice_id: int | None = None

    payment_number: str = Field(
        max_length=50,
    )

    payment_date: date

    amount: Decimal = Field(
        gt=0,
    )

    payment_method: PaymentMethod

    reference: str | None = None

    notes: str | None = None


class PaymentUpdate(BaseModel):
    payment_date: date

    amount: Decimal = Field(
        gt=0,
    )

    payment_method: PaymentMethod

    reference: str | None = None

    notes: str | None = None

    status: PaymentStatus


class PaymentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    organization_id: int

    customer_id: int

    invoice_id: int | None

    payment_number: str

    payment_date: date

    amount: Decimal

    payment_method: PaymentMethod

    reference: str | None

    notes: str | None

    status: PaymentStatus

    created_by: int | None

    updated_by: int | None