from unittest.mock import patch


@patch("app.api.routers.ai.generate_ai_response_with_tools")
def test_chat_endpoint_returns_ai_response(mock_generate, client):
    mock_generate.return_value = "Python is a programming language."

    response = client.post("/api/ai/chat", json={
        "message": "What is Python?",
        "conversation_id": "conv1",
    })

    assert response.status_code == 200
    assert response.json() == {
        "response": "Python is a programming language.",
        "conversation_id": "conv1",
    }
    mock_generate.assert_called_once()