from sqlmodel import Session, SQLModel, create_engine
from app.models.book import Book
from app.services.ai_context import build_book_context

engine = create_engine("sqlite://", connect_args={"check_same_thread": False})


def setup_module():
    SQLModel.metadata.create_all(engine)


def _seed_books(session):
    books = [
        Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True),
        Book(title="Clean Code", author="Robert Martin", category="Tech", year=2008, available=True),
    ]
    session.add_all(books)
    session.commit()


def test_build_book_context_returns_ai_friendly_structure():
    with Session(engine) as session:
        _seed_books(session)
        context = build_book_context(session, title="python")

        assert len(context) == 1
        assert context[0] == {
            "id": context[0]["id"],
            "title": "Learn Python",
            "author": "Guido",
            "category": "Programming",
            "year": 2020,
            "available": True,
        }


def test_build_book_context_no_match_returns_empty_list():
    with Session(engine) as session:
        context = build_book_context(session, title="Nonexistent")
        assert context == []


def test_build_book_context_no_filters_returns_all():
    with Session(engine) as session:
        context = build_book_context(session)
        assert len(context) == 2