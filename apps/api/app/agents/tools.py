from decimal import Decimal
from sqlalchemy.orm import Session

from app.customers.repository import count_customers
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

# -----------------------------
# BUSINESS SUMMARY
# -----------------------------
def get_business_summary(
    db: Session,
    organization_id: int,
) -> dict:

    return {
        "customers": count_customers(db, organization_id),
        "invoices": count_invoices(db, organization_id),
        "payments": count_payments(db, organization_id),
        "revenue": float(total_revenue(db, organization_id)),
        "outstanding": float(total_outstanding(db, organization_id)),
    }


# -----------------------------
# REVENUE
# -----------------------------
def get_revenue(
    db: Session,
    organization_id: int,
) -> float:

    return float(total_revenue(db, organization_id))


# -----------------------------
# COUNTERS
# -----------------------------
def get_customer_count(
    db: Session,
    organization_id: int,
) -> int:

    return count_customers(db, organization_id)


def get_invoice_count(
    db: Session,
    organization_id: int,
) -> int:

    return count_invoices(db, organization_id)


def get_payment_count(
    db: Session,
    organization_id: int,
) -> int:

    return count_payments(db, organization_id)


# -----------------------------
# PAYMENTS
# -----------------------------
def get_payment_total(
    db: Session,
    organization_id: int,
) -> float:

    return float(total_payments(db, organization_id))


# -----------------------------
# OUTSTANDING
# -----------------------------
def get_outstanding_amount(
    db: Session,
    organization_id: int,
) -> float:

    return float(total_outstanding(db, organization_id))


# -----------------------------
# UNPAID INVOICES
# -----------------------------
def get_unpaid_invoices(
    db: Session,
    organization_id: int,
):

    invoices = unpaid_invoices(db, organization_id)

    return [
        {
            "invoice_number": i.invoice_number,
            "customer_id": i.customer_id,
            "total": float(i.total),
            "status": str(i.status),
            "due_date": i.due_date.isoformat(),
        }
        for i in invoices
    ]