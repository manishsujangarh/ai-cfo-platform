from decimal import Decimal

from sqlalchemy.orm import Session

from app.accounts.repository import get_by_code

from app.accounts.constants import (
    ACCOUNTS_RECEIVABLE,
    SALES_REVENUE,
    GST_PAYABLE,
)

from app.invoices.model import Invoice

from app.journal_entries.schema import (
    JournalEntryCreate,
    JournalEntryLineCreate,
)

from app.journal_entries.service import (
    create as create_journal,
)


def post_invoice(
    db: Session,
    invoice: Invoice,
):
    ar = get_by_code(
        db,
        invoice.organization_id,
        ACCOUNTS_RECEIVABLE,
    )

    sales = get_by_code(
        db,
        invoice.organization_id,
        SALES_REVENUE,
    )

    gst = get_by_code(
        db,
        invoice.organization_id,
        GST_PAYABLE,
    )

    if ar is None:
        raise ValueError("Accounts Receivable account not found")

    if sales is None:
        raise ValueError("Sales Revenue account not found")

    if invoice.tax > Decimal("0.00") and gst is None:
       raise ValueError("GST Payable account not found")

    lines = [
        JournalEntryLineCreate(
            account_id=ar.id,
            debit=invoice.total,
            credit=Decimal("0.00"),
            description="Accounts Receivable",
        ),
        JournalEntryLineCreate(
            account_id=sales.id,
            debit=Decimal("0.00"),
            credit=invoice.subtotal,
            description="Sales Revenue",
        ),
    ]

    if invoice.tax > Decimal("0.00"):
        lines.append(
            JournalEntryLineCreate(
                account_id=gst.id,
                debit=Decimal("0.00"),
                credit=invoice.tax,
                description="GST Payable",
            )
        )

    journal = JournalEntryCreate(
        organization_id=invoice.organization_id,
        entry_date=invoice.invoice_date,
        reference=invoice.invoice_number,
        description=f"Invoice {invoice.invoice_number}",
        lines=lines,
    )

    return create_journal(
        db,
        journal,
    )