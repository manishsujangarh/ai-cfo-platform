from sqlalchemy.orm import Session

from app.dashboard.schemas import DashboardSummary

from app.customers.repository import count_customers
from app.vendors.repository import count_vendors

from app.invoices.repository import (
    count_invoices,
    total_revenue,
    total_outstanding,
)

from app.payments.repository import (
    count_payments,
    total_payments,
)

from app.organization_members.repository import get_by_user_id


def get_dashboard_summary(
    db: Session,
    user_id: int,
) -> DashboardSummary:

    membership = get_by_user_id(
        db=db,
        user_id=user_id,
    )

    if membership is None:
        raise ValueError("Organization membership not found")

    organization_id = membership.organization_id

    return DashboardSummary(
        customers=count_customers(db, organization_id),
        vendors=count_vendors(db, organization_id),
        invoices=count_invoices(db, organization_id),
        payments=count_payments(db, organization_id),
        revenue=total_revenue(db, organization_id),
        payments_received=total_payments(db, organization_id),
        outstanding=total_outstanding(db, organization_id),
    )