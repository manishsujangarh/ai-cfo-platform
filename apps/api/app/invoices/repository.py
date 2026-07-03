from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload
from decimal import Decimal

from app.invoices.model import Invoice


from app.common.enums import InvoiceStatus

def create(
    db: Session,
    invoice: Invoice,
) -> Invoice:
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


def get_by_id(
    db: Session,
    invoice_id: int,
) -> Invoice | None:

    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.items)
        )
        .where(
            Invoice.id == invoice_id
        )
    )

    return db.scalar(statement)


def get_by_invoice_number(
    db: Session,
    organization_id: int,
    invoice_number: str,
) -> Invoice | None:

    statement = (
        select(Invoice)
        .where(
            Invoice.organization_id == organization_id,
            Invoice.invoice_number == invoice_number,
        )
    )

    return db.scalar(statement)


def list_all(
    db: Session,
) -> list[Invoice]:

    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.items)
        )
        .order_by(
            Invoice.id.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def list_by_organization(
    db: Session,
    organization_id: int,
) -> list[Invoice]:

    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.items)
        )
        .where(
            Invoice.organization_id == organization_id
        )
        .order_by(
            Invoice.invoice_date.desc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def update(
    db: Session,
    invoice: Invoice,
) -> Invoice:

    db.commit()
    db.refresh(invoice)

    return invoice


def delete(
    db: Session,
    invoice: Invoice,
) -> None:

    db.delete(invoice)
    db.commit()


def count_invoices(
    db: Session,
    organization_id: int,
) -> int:
    statement = (
        select(func.count(Invoice.id))
        .where(
            Invoice.organization_id == organization_id
        )
    )

    return db.scalar(statement) or 0


def total_revenue(
    db: Session,
    organization_id: int,
) -> Decimal:
    statement = (
        select(func.sum(Invoice.total))
        .where(
            Invoice.organization_id == organization_id,
        )
    )

    return db.scalar(statement) or Decimal("0.00")





def unpaid_invoices(
    db: Session,
    organization_id: int,
) -> list[Invoice]:
    statement = (
        select(Invoice)
        .where(
            Invoice.organization_id == organization_id,
            Invoice.status.in_(
                [
                    InvoiceStatus.SENT,
                    InvoiceStatus.PARTIALLY_PAID,
                    InvoiceStatus.OVERDUE,
                ]
            ),
        )
        .order_by(
            Invoice.due_date.asc()
        )
    )

    return list(db.scalars(statement).all())


def total_outstanding(
    db: Session,
    organization_id: int,
) -> Decimal:
    statement = (
        select(func.sum(Invoice.total))
        .where(
            Invoice.organization_id == organization_id,
            Invoice.status.in_(
                [
                    InvoiceStatus.SENT,
                    InvoiceStatus.PARTIALLY_PAID,
                    InvoiceStatus.OVERDUE,
                ]
            ),
        )
    )

    return db.scalar(statement) or Decimal("0.00")