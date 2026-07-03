from sqlalchemy.orm import Session

from app.agents.registry import TOOLS


def chat(
    db: Session,
    organization_id: int,
    message: str,
) -> dict:

    text = message.lower()

    if "summary" in text:
        result = TOOLS["business_summary"](
            db,
            organization_id,
        )

        return {
            "answer": result,
        }

    if "customer" in text:
        result = TOOLS["customer_count"](
            db,
        )

        return {
            "answer": f"You have {result} customers.",
        }

    if "invoice" in text:
        result = TOOLS["invoice_count"](
            db,
        )

        return {
            "answer": f"You have {result} invoices.",
        }

    if "payment" in text:
        result = TOOLS["payment_count"](
            db,
        )

        return {
            "answer": f"You have {result} payments.",
        }

    if "revenue" in text:
        result = TOOLS["revenue"](
            db,
            organization_id,
        )

        return {
            "answer": f"Total revenue is ₹{result}.",
        }

    if "outstanding" in text:
        result = TOOLS["outstanding"](
            db,
            organization_id,
        )

        return {
            "answer": f"Outstanding amount is ₹{result}.",
        }

    if "unpaid" in text:
        result = TOOLS["unpaid_invoices"](
            db,
            organization_id,
        )

        return {
            "answer": result,
        }

    return {
        "answer": "I don't understand that request yet.",
    }