from datetime import date
from decimal import Decimal
import enum

from sqlalchemy import Date, ForeignKey, Numeric, String, UniqueConstraint,Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import (
    AuditMixin,
    OrganizationMixin,
    TimestampMixin,
)
from app.common.enums import InvoiceStatus
class Invoice(Base,
    TimestampMixin,
    AuditMixin,
    OrganizationMixin):
    __tablename__ = "invoices"

    __table_args__ = (
        UniqueConstraint(
            "organization_id", 
            "invoice_number", 
            name="uq_invoice_number_per_org"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        index=True,
        nullable=False,
    )

    invoice_number: Mapped[str] = mapped_column(
        String(50),
       
        index=True,
        nullable=False,
    )

    invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )


    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus),
        default=InvoiceStatus.DRAFT,
        index=True,
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),    
        default=Decimal("0.00"),
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    items: Mapped[list["InvoiceItem"]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False,
    )

    product_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    tax_rate: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("1.00"),
        nullable=False,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    invoice: Mapped["Invoice"] = relationship(
        back_populates="items",
    )


    