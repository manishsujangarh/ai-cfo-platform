from decimal import Decimal

from app.invoices.model import InvoiceItem
from app.invoices.schema import InvoiceItemCreate


def calculate_invoice(
    items: list[InvoiceItemCreate],
):
    invoice_items: list[InvoiceItem] = []

    subtotal = Decimal("0.00")
    discount = Decimal("0.00")
    tax = Decimal("0.00")

    for item in items:

        line_amount = (
            item.quantity
            * item.unit_price
        )

        line_discount = item.discount

        taxable_amount = (
            line_amount
            - line_discount
        )

        line_tax = (
            taxable_amount
            * item.tax_rate
            / Decimal("100")
        )

        line_total = (
            taxable_amount
            + line_tax
        )

        subtotal += line_amount
        discount += line_discount
        tax += line_tax

        invoice_items.append(
            InvoiceItem(
                product_name=item.product_name,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                discount=item.discount,
                tax_rate=item.tax_rate,
                line_total=line_total,
            )
        )

    total = (
        subtotal
        - discount
        + tax
    )

    return (
        invoice_items,
        subtotal,
        discount,
        tax,
        total,
    )