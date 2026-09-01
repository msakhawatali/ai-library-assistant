from unittest.mock import patch


@patch("app.api.routers.ai.extract_search_filters")
@patch("app.api.routers.ai.generate_ai_response")
def test_chat_response_includes_conversation_id(mock_generate, mock_extract, client):
    mock_extract.return_value = {}
    mock_generate.return_value = "Some response"

    response = client.post("/api/ai/chat", json={
        "message": "Hello",
        "conversation_id": "conv-xyz-123",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == "conv-xyz-123"
    assert data["response"] == "Some response"