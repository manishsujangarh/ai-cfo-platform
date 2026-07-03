from sqlalchemy.orm import Session

from app.journal_entries.model import JournalEntry


def create(
    db: Session,
    entry: JournalEntry,
) -> JournalEntry:
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def get_by_id(
    db: Session,
    journal_entry_id: int,
) -> JournalEntry | None:
    return (
        db.query(JournalEntry)
        .filter(
            JournalEntry.id == journal_entry_id,
        )
        .first()
    )


def list_all(
    db: Session,
) -> list[JournalEntry]:
    return (
        db.query(JournalEntry)
        .order_by(
            JournalEntry.id.desc()
        )
        .all()
    )


def update(
    db: Session,
    entry: JournalEntry,
) -> JournalEntry:
    db.commit()
    db.refresh(entry)

    return entry


def delete(
    db: Session,
    entry: JournalEntry,
) -> None:
    db.delete(entry)
    db.commit()