from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ----------------------------
# Journal Entry Line
# ----------------------------

class JournalEntryLineCreate(BaseModel):
    account_id: int
    description: str | None = None

    debit: Decimal = Field(default=Decimal("0.00"), ge=0)
    credit: Decimal = Field(default=Decimal("0.00"), ge=0)


class JournalEntryLineResponse(BaseModel):
    id: int
    account_id: int
    description: str | None

    debit: Decimal
    credit: Decimal

    model_config = ConfigDict(
        from_attributes=True,
    )


# ----------------------------
# Create Journal Entry
# ----------------------------

class JournalEntryCreate(BaseModel):
    organization_id: int

    entry_date: date

    reference: str | None = None

    description: str

    lines: list[JournalEntryLineCreate]


# ----------------------------
# Update Draft Journal Entry
# ----------------------------

class JournalEntryUpdate(BaseModel):
    entry_date: date

    reference: str | None = None

    description: str

    lines: list[JournalEntryLineCreate]


# ----------------------------
# Response
# ----------------------------

class JournalEntryResponse(BaseModel):
    id: int

    organization_id: int

    entry_date: date

    reference: str | None

    description: str

    status: str

    lines: list[JournalEntryLineResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )