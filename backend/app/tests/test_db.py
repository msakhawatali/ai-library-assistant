from sqlmodel import Session, create_engine, SQLModel
from app.models.book import Book

engine = create_engine("sqlite://", connect_args={"check_same_thread": False})

def setup_module():
    SQLModel.metadata.create_all(engine)

def test_insert_and_fetch_book():
    with Session(engine) as session:
        book = Book(title="Clean Code", author="Robert Martin", category="Tech", year=2008)
        session.add(book)
        session.commit()
        session.refresh(book)

        assert book.id is not None
        result = session.get(Book, book.id)
        assert result.title == "Clean Code"