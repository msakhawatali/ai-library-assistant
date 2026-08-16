from sqlmodel import Session, SQLModel, create_engine
from app.models.book import Book
from app.services.book_search import search_books

engine = create_engine("sqlite://", connect_args={"check_same_thread": False})


def setup_module():
    SQLModel.metadata.create_all(engine)


def _seed_books(session):
    books = [
        Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True),
        Book(title="Advanced Python", author="Guido", category="Programming", year=2022, available=False),
        Book(title="Clean Code", author="Robert Martin", category="Tech", year=2008, available=True),
    ]
    session.add_all(books)
    session.commit()


def test_search_by_title():
    with Session(engine) as session:
        _seed_books(session)
        results = search_books(session, title="python")
        assert len(results) == 2


def test_search_by_author_and_availability():
    with Session(engine) as session:
        results = search_books(session, author="Guido", available=True)
        assert len(results) == 1
        assert results[0].title == "Learn Python"


def test_search_no_match_returns_empty_list():
    with Session(engine) as session:
        results = search_books(session, title="Nonexistent Book Title")
        assert results == []


def test_search_no_filters_returns_all():
    with Session(engine) as session:
        results = search_books(session)
        assert len(results) == 3