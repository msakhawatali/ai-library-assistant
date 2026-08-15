from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.db.database import get_session

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


def setup_module():
    SQLModel.metadata.create_all(engine)


client = TestClient(app)


def test_create_book():
    response = client.post("/api/books", json={
        "title": "Clean Code", "author": "Robert Martin", "category": "Tech", "year": 2008
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Clean Code"


def test_get_books():
    response = client.get("/api/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_book_not_found():
    response = client.get("/api/books/9999")
    assert response.status_code == 404


def test_update_book():
    create_res = client.post("/api/books", json={
        "title": "Old Title", "author": "A", "category": "C", "year": 2000
    })
    book_id = create_res.json()["id"]

    update_res = client.patch(f"/api/books/{book_id}", json={"title": "New Title"})
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "New Title"


def test_delete_book():
    create_res = client.post("/api/books", json={
        "title": "To Delete", "author": "A", "category": "C", "year": 2001
    })
    book_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/books/{book_id}")
    assert delete_res.status_code == 204

    get_res = client.get(f"/api/books/{book_id}")
    assert get_res.status_code == 404