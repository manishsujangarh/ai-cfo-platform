from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from apps.api.app.journal_entries.schema import JournalEntryLineCreate


# ----------------------------
# Invoice Item
# ----------------------------

class InvoiceItemCreate(BaseModel):
    invoice_id: int
    product_name: str | None = None

    description: str | None = None
    unit_price: Decimal = Field(default=Decimal("0.00"), ge=0)
    tax_rate: Decimal = Field(default=Decimal("0.00"), ge=0)
    line_total: Decimal = Field(default=Decimal("0.00"), ge=0)
    quantity: Decimal = Field(default=Decimal("1.00"), ge=0)
    discount: Decimal = Field(default=Decimal("0.00"), ge=0)



class InvoiceItemResponse(BaseModel):
    id: int
    invoice_id: int
    product_name: str | None

    description: str | None

    unit_price: Decimal
    tax_rate: Decimal
    line_total: Decimal
    quantity: Decimal
    discount: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


# ----------------------------
# Create Invoice
# ----------------------------

class InvoiceCreate(BaseModel):
    organization_id: int

    customer_id: int

    invoice_number: str | None = None

    invoice_date: date

    due_date: date

    status: str = "draft"


    subtotal: Decimal = Field(default=Decimal("0.00"), ge=0)

    tax: Decimal = Field(default=Decimal("0.00"), ge=0)

    discount: Decimal = Field(default=Decimal("0.00"), ge=0)

    total: Decimal = Field(default=Decimal("0.00"), ge=0)

    notes: str | None = None


    items: list[InvoiceItemCreate]


# ----------------------------
# Update Draft Invoice 
# ----------------------------

class InvoiceUpdate(BaseModel):
    entry_date: date

    invoice_number: str | None = None
    
    description: str

    status: str = "draft"

    due_date: date

    subtotal: Decimal = Field(default=Decimal("0.00"), ge=0)

    tax: Decimal = Field(default=Decimal("0.00"), ge=0)

    discount: Decimal = Field(default=Decimal("0.00"), ge=0)

    total: Decimal = Field(default=Decimal("0.00"), ge=0)

    notes: str | None = None

    items: list[InvoiceItemCreate]


# ----------------------------
# Response
# ----------------------------

class InvoiceResponse(BaseModel):
    id: int

    organization_id: int

    entry_date: date

    invoice_number: str | None

    description: str

    status: str

    items: list[InvoiceItemResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )