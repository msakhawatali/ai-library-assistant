from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book import (
    create_book,
    delete_book,
    get_book,
    get_books,
    update_book,
)

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_new_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
):
    return create_book(book_data, session)


@router.get("/", response_model=list[BookRead])
def read_books(
    session: Session = Depends(get_session),
):
    return get_books(session)


@router.get("/{book_id}", response_model=BookRead)
def read_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    book = get_book(book_id, session)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_existing_book(
    book_id: int,
    book_data: BookUpdate,
    session: Session = Depends(get_session),
):
    book = get_book(book_id, session)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return update_book(book, book_data, session)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    book = get_book(book_id, session)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    delete_book(book, session)