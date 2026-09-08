from unittest.mock import patch, MagicMock
from app.services.ai_service import AIServiceError


@patch("app.services.ai_service.get_openai_client")
def test_book_search_request_triggers_tool(mock_get_client, client, session):
    from app.models.book import Book
    session.add(Book(title="Learn Python", author="Guido", category="Programming", year=2020, available=True))
    session.commit()

    mock_client = MagicMock()

    tool_call = MagicMock()
    tool_call.id = "call_1"
    tool_call.function.arguments = '{"title": "python"}'
    first_response = MagicMock()
    first_response.choices[0].message.tool_calls = [tool_call]
    first_response.choices[0].message.content = None

    second_response = MagicMock()
    second_response.choices[0].message.tool_calls = None
    second_response.choices[0].message.content = "Yes, we have Learn Python by Guido."

    mock_client.chat.completions.create.side_effect = [first_response, second_response]
    mock_get_client.return_value = mock_client

    response = client.post("/api/ai/chat", json={
        "message": "Do you have Python books?",
        "conversation_id": "conv-tool-test",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Yes, we have Learn Python by Guido."
    assert data["conversation_id"] == "conv-tool-test"
    assert mock_client.chat.completions.create.call_count == 2


@patch("app.services.ai_service.get_openai_client")
def test_off_topic_request_does_not_trigger_tool(mock_get_client, client):
    mock_client = MagicMock()

    response_obj = MagicMock()
    response_obj.choices[0].message.tool_calls = None
    response_obj.choices[0].message.content = "I'm doing well, thank you!"

    mock_client.chat.completions.create.return_value = response_obj
    mock_get_client.return_value = mock_client

    response = client.post("/api/ai/chat", json={
        "message": "How are you?",
        "conversation_id": "conv-offtopic-test",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "I'm doing well, thank you!"
    assert data["conversation_id"] == "conv-offtopic-test"
    assert mock_client.chat.completions.create.call_count == 1


@patch("app.api.routers.ai.generate_ai_response_with_tools")
def test_ai_service_error_returns_503(mock_generate, client):
    mock_generate.side_effect = AIServiceError(
        "AI service is currently unavailable. Please try again later."
    )

    response = client.post("/api/ai/chat", json={
        "message": "What is Python?",
        "conversation_id": "conv-error-test",
    })

    assert response.status_code == 503
    assert response.json()["detail"] == "AI service is currently unavailable. Please try again later."