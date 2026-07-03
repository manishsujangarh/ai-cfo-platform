from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.journal_entries.schema import (
    JournalEntryCreate,
    JournalEntryResponse,
    JournalEntryUpdate,
)

from app.journal_entries.service import (
    create,
    delete,
    get,
    list_all,
    post,
    update,
)

router = APIRouter(
    prefix="/journal-entries",
    tags=["Journal Entries"],
)


@router.post(
    "",
    response_model=JournalEntryResponse,
    status_code=201,
)
def create_journal_entry(
    request: JournalEntryCreate,
    db: Session = Depends(get_db),
):
    return create(
        db,
        request,
    )


@router.get(
    "",
    response_model=list[JournalEntryResponse],
)
def get_journal_entries(
    db: Session = Depends(get_db),
):
    return list_all(db)


@router.get(
    "/{journal_entry_id}",
    response_model=JournalEntryResponse,
)
def get_journal_entry(
    journal_entry_id: int,
    db: Session = Depends(get_db),
):

    entry = get(
        db,
        journal_entry_id,
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Journal entry not found",
        )

    return entry


@router.put(
    "/{journal_entry_id}",
    response_model=JournalEntryResponse,
)
def update_journal_entry(
    journal_entry_id: int,
    request: JournalEntryUpdate,
    db: Session = Depends(get_db),
):
    return update(
        db,
        journal_entry_id,
        request,
    )


@router.delete(
    "/{journal_entry_id}",
    status_code=204,
)
def delete_journal_entry(
    journal_entry_id: int,
    db: Session = Depends(get_db),
):
    delete(
        db,
        journal_entry_id,
    )


@router.post(
    "/{journal_entry_id}/post",
    response_model=JournalEntryResponse,
)
def post_journal_entry(
    journal_entry_id: int,
    db: Session = Depends(get_db),
):
    return post(
        db,
        journal_entry_id,
    )