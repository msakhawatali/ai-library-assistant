from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.api.routers.ai.generate_ai_response")
def test_chat_endpoint_returns_ai_response(mock_generate):
    mock_generate.return_value = "Python is a programming language."

    response = client.post("/api/ai/chat", json={"message": "What is Python?"})

    assert response.status_code == 200
    assert response.json() == {"response": "Python is a programming language."}
    mock_generate.assert_called_once_with("What is Python?", book_context=[])


@patch("app.services.ai_service.get_openai_client")
def test_generate_ai_response_calls_openai_client(mock_get_client):
    from app.services.ai_service import generate_ai_response

    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "Mocked response"
    mock_client.chat.completions.create.return_value = mock_completion
    mock_get_client.return_value = mock_client

    result = generate_ai_response("Hello")

    assert result == "Mocked response"