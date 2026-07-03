from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.accounts.repository import get_by_id as get_account_by_id

from app.journal_entries.model import (
    JournalEntry,
    JournalEntryLine,
)

from app.journal_entries.repository import (
    create as repository_create,
    delete as repository_delete,
    get_by_id,
    list_all as repository_list_all,
    update as repository_update,
)

from app.journal_entries.schema import (
    JournalEntryCreate,
    JournalEntryUpdate,
)


def create(
    db: Session,
    request: JournalEntryCreate,
):
    total_debit = Decimal("0.00")
    total_credit = Decimal("0.00")

    journal = JournalEntry(
        organization_id=request.organization_id,
        entry_date=request.entry_date,
        reference=request.reference,
        description=request.description,
        status="posted",
    )

    for line in request.lines:
        account = get_account_by_id(
            db,
            line.account_id,
        )

        if account is None:
            raise HTTPException(
                status_code=404,
                detail=f"Account {line.account_id} not found",
            )

        total_debit += line.debit
        total_credit += line.credit

        journal.lines.append(
            JournalEntryLine(
                account_id=line.account_id,
                description=line.description,
                debit=line.debit,
                credit=line.credit,
            )
        )

    if total_debit != total_credit:
        raise HTTPException(
            status_code=400,
            detail="Debit and Credit must be equal",
        )

    return repository_create(
        db,
        journal,
    )


def get(
    db: Session,
    journal_entry_id: int,
):
    return get_by_id(
        db,
        journal_entry_id,
    )


def list_all(
    db: Session,
):
    return repository_list_all(
        db,
    )


def update(
    db: Session,
    journal_entry_id: int,
    request: JournalEntryUpdate,
):
    journal = get_by_id(
        db,
        journal_entry_id,
    )

    if journal is None:
        raise HTTPException(
            status_code=404,
            detail="Journal Entry not found",
        )

    journal.entry_date = request.entry_date
    journal.reference = request.reference
    journal.description = request.description

    journal.lines.clear()

    total_debit = Decimal("0.00")
    total_credit = Decimal("0.00")

    for line in request.lines:
        account = get_account_by_id(
            db,
            line.account_id,
        )

        if account is None:
            raise HTTPException(
                status_code=404,
                detail=f"Account {line.account_id} not found",
            )

        total_debit += line.debit
        total_credit += line.credit

        journal.lines.append(
            JournalEntryLine(
                account_id=line.account_id,
                description=line.description,
                debit=line.debit,
                credit=line.credit,
            )
        )

    if total_debit != total_credit:
        raise HTTPException(
            status_code=400,
            detail="Debit and Credit must be equal",
        )

    return repository_update(
        db,
        journal,
    )


def delete(
    db: Session,
    journal_entry_id: int,
):
    journal = get_by_id(
        db,
        journal_entry_id,
    )

    if journal is None:
        raise HTTPException(
            status_code=404,
            detail="Journal Entry not found",
        )

    repository_delete(
        db,
        journal,
    )