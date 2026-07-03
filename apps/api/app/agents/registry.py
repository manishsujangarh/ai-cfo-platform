from app.agents.tools import (
    get_business_summary,
    get_customer_count,
    get_vendor_count,
    get_invoice_count,
    get_payment_count,
    get_payment_total,
    get_revenue,
    get_outstanding_amount,
    get_unpaid_invoices,
)

TOOLS = {
    "business_summary": get_business_summary,
    "customer_count": get_customer_count,
    "vendor_count": get_vendor_count,
    "invoice_count": get_invoice_count,
    "payment_count": get_payment_count,
    "payment_total": get_payment_total,
    "revenue": get_revenue,
    "outstanding": get_outstanding_amount,
    "unpaid_invoices": get_unpaid_invoices,
}