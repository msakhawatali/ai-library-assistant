from typing import Optional
from sqlmodel import Session, select
from app.models.book import Book


def search_books(
    session: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    available: Optional[bool] = None,
) -> list[Book]:
    query = select(Book)

    if title:
        query = query.where(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.where(Book.author.ilike(f"%{author}%"))
    if category:
        query = query.where(Book.category.ilike(f"%{category}%"))
    if year is not None:
        query = query.where(Book.year == year)
    if available is not None:
        query = query.where(Book.available == available)

    return session.exec(query).all()