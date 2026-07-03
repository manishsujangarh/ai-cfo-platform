import enum



class JournalEntryStatus(str, enum.Enum):
    DRAFT = "draft"
    POSTED = "posted"


class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"