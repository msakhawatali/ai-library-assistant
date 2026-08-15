from sqlmodel import Session, select

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


def create_book(book_data: BookCreate, session: Session) -> Book:
    book = Book(**book_data.model_dump())

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


def get_books(session: Session) -> list[Book]:
    statement = select(Book)
    return list(session.exec(statement).all())


def get_book(book_id: int, session: Session) -> Book | None:
    return session.get(Book, book_id)


def update_book(
    book: Book,
    book_data: BookUpdate,
    session: Session,
) -> Book:
    update_data = book_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


def delete_book(book: Book, session: Session) -> None:
    session.delete(book)
    session.commit()