from sqlalchemy.orm import Session

from app.payments.model import Payment


def create(
    db: Session,
    payment: Payment,
) -> Payment:
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def get_by_id(
    db: Session,
    payment_id: int,
) -> Payment | None:
    return (
        db.query(Payment)
        .filter(
            Payment.id == payment_id,
        )
        .first()
    )


def get_by_payment_number(
    db: Session,
    payment_number: str,
) -> Payment | None:
    return (
        db.query(Payment)
        .filter(
            Payment.payment_number == payment_number,
        )
        .first()
    )


def list_all(
    db: Session,
) -> list[Payment]:
    return (
        db.query(Payment)
        .order_by(
            Payment.id.desc(),
        )
        .all()
    )


def update(
    db: Session,
    payment: Payment,
) -> Payment:
    db.commit()
    db.refresh(payment)

    return payment


def delete(
    db: Session,
    payment: Payment,
) -> None:
    db.delete(payment)
    db.commit()