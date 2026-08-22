from sqlmodel import Session, delete
from app.models.book import Book
from app.services.ai_context import build_book_context
from app.tests.conftest import engine

def _clear_books():
    with Session(engine) as session:
        session.exec(delete(Book))
        session.commit()


def _seed_books(session):
    books = [
        Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True),
        Book(title="Clean Code", author="Robert Martin", category="Tech", year=2008, available=True),
    ]
    session.add_all(books)
    session.commit()


def test_build_book_context_returns_ai_friendly_structure():
    _clear_books()
    with Session(engine) as session:
        _seed_books(session)
        context = build_book_context(session, title="python")

        assert len(context) == 1
        assert context[0]["title"] == "Learn Python"


def test_build_book_context_no_match_returns_empty_list():
    _clear_books()
    with Session(engine) as session:
        context = build_book_context(session, title="Nonexistent")
        assert context == []


def test_build_book_context_no_filters_returns_all():
    _clear_books()
    with Session(engine) as session:
        _seed_books(session)
        context = build_book_context(session)
        assert len(context) == 2