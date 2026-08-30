from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel
from sqlmodel.pool import StaticPool
from app.services.ai_service import AIServiceError

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


@patch("app.api.routers.ai.extract_search_filters")
@patch("app.api.routers.ai.generate_ai_response")
def test_chat_uses_extracted_filters(mock_generate, mock_extract, client, session):
    from app.models.book import Book
    session.add(Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True))
    session.commit()

    mock_extract.return_value = {"title": "python"}
    mock_generate.return_value = "Yes, we have Learn Python."

    response = client.post("/api/ai/chat", json={
    "message": "Do you have Python books?",
    "conversation_id": "conv1",
    })

    assert response.status_code == 200
    passed_context = mock_generate.call_args.kwargs["book_context"]
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

@patch("app.api.routers.ai.get_history")
@patch("app.api.routers.ai.extract_search_filters")
@patch("app.api.routers.ai.generate_ai_response")
def test_chat_includes_previous_messages(mock_generate, mock_extract, mock_get_history, client, session):
    from app.schemas.chat import ChatMessage

    mock_extract.return_value = {}
    mock_get_history.return_value = [
        ChatMessage(role="user", content="What Python books are available?"),
        ChatMessage(role="assistant", content="Here are the available Python books..."),
    ]
    mock_generate.return_value = "The beginner one is easier."

    response = client.post("/api/ai/chat", json={
        "message": "Which one is better for beginners?",
        "conversation_id": "conv1",
    })

    assert response.status_code == 200
    passed_history = mock_generate.call_args.kwargs["history"]
    assert len(passed_history) == 2
    assert passed_history[0].content == "What Python books are available?"


@patch("app.api.routers.ai.extract_search_filters")
@patch("app.api.routers.ai.generate_ai_response")
def test_chat_endpoint_returns_503_on_ai_service_error(mock_generate, mock_extract, client):
    mock_extract.return_value = {}
    mock_generate.side_effect = AIServiceError("AI service is currently unavailable. Please try again later.")

    response = client.post("/api/ai/chat", json={
        "message": "What is Python?",
        "conversation_id": "conv-error-test",
    })

    assert response.status_code == 503
    assert response.json()["detail"] == "AI service is currently unavailable. Please try again later."
    # Confirm koi internal detail leak nahi hui
    assert "traceback" not in response.text.lower()
    assert "api_key" not in response.text.lower()