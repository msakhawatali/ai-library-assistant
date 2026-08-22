from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel
from sqlmodel.pool import StaticPool

from app.main import app
from app.db.database import get_session
from app.models.book import Book
from app.tests.conftest import engine


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


def setup_module():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True))
        session.commit()


client = TestClient(app)


@patch("app.api.routers.ai.generate_ai_response")
def test_chat_uses_book_context(mock_generate):
    mock_generate.return_value = "Yes, we have Learn Python by Guido."

    response = client.post("/api/ai/chat", json={"message": "Do you have Python books?"})

    assert response.status_code == 200
    assert response.json() == {"response": "Yes, we have Learn Python by Guido."}

    call_args = mock_generate.call_args
    passed_context = call_args.kwargs["book_context"]
    assert any(b["title"] == "Learn Python" for b in passed_context)
    passed_context = call_args.kwargs.get("book_context") or call_args.args[1]
    assert any(b["title"] == "Learn Python" for b in passed_context)


@patch("app.services.ai_service.get_openai_client")
def test_generate_ai_response_handles_no_books(mock_get_client):
    from app.services.ai_service import generate_ai_response

    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "No books found."
    mock_client.chat.completions.create.return_value = mock_completion
    mock_get_client.return_value = mock_client

    result = generate_ai_response("Do you have anything?", book_context=[])
    assert result == "No books found."