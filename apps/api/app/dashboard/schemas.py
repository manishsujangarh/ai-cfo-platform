from decimal import Decimal

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    customers: int
    vendors: int

    invoices: int
    payments: int

    revenue: Decimal
    payments_received: Decimal
    outstanding: Decimal