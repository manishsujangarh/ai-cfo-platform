from decimal import Decimal

from sqlalchemy.orm import Session

from app.customers.repository import (
    count_customers,
)

from app.invoices.repository import (
    count_invoices,
    total_revenue,
    total_outstanding,
    unpaid_invoices,
)

from app.payments.repository import (
    count_payments,
    total_payments,
)


def get_business_summary(
    db: Session,
    organization_id: int,
) -> dict:

    return {
        "customers": count_customers(db),
        "invoices": count_invoices(db),
        "payments": count_payments(db),
        "revenue": str(
            total_revenue(
                db,
                organization_id,
            )
        ),
        "outstanding": str(
            total_outstanding(
                db,
                organization_id,
            )
        ),
    }


def get_revenue(
    db: Session,
    organization_id: int,
) -> Decimal:

    return total_revenue(
        db,
        organization_id,
    )


def get_customer_count(
    db: Session,
) -> int:

    return count_customers(db)


def get_invoice_count(
    db: Session,
) -> int:

    return count_invoices(db)


def get_payment_count(
    db: Session,
) -> int:

    return count_payments(db)


def get_payment_total(
    db: Session,
    organization_id: int,
) -> Decimal:

    return total_payments(
        db,
        organization_id,
    )


def get_outstanding_amount(
    db: Session,
    organization_id: int,
) -> Decimal:

    return total_outstanding(
        db,
        organization_id,
    )


def get_unpaid_invoices(
    db: Session,
    organization_id: int,
):

    invoices = unpaid_invoices(
        db,
        organization_id,
    )

    return [
        {
            "invoice_number": invoice.invoice_number,
            "customer_id": invoice.customer_id,
            "total": str(invoice.total),
            "status": invoice.status,
            "due_date": str(invoice.due_date),
        }
        for invoice in invoices
    ]