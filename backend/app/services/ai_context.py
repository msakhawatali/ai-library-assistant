from typing import Optional
from sqlmodel import Session
from app.services.book_search import search_books


def build_book_context(
    session: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    available: Optional[bool] = None,
) -> list[dict]:
    books = search_books(
        session,
        title=title,
        author=author,
        category=category,
        year=year,
        available=available,
    )

    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "year": book.year,
            "available": book.available,
        }
        for book in books
    ]