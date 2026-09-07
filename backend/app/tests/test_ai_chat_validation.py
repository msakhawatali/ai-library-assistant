def test_chat_rejects_empty_message(client):
    response = client.post("/api/ai/chat", json={
        "message": "",
        "conversation_id": "conv-1",
    })
    assert response.status_code == 422


def test_chat_rejects_whitespace_only_message(client):
    response = client.post("/api/ai/chat", json={
        "message": "   ",
        "conversation_id": "conv-1",
    })
    assert response.status_code == 422


def test_chat_rejects_empty_conversation_id(client):
    response = client.post("/api/ai/chat", json={
        "message": "What is Python?",
        "conversation_id": "",
    })
    assert response.status_code == 422


def test_chat_rejects_whitespace_only_conversation_id(client):
    response = client.post("/api/ai/chat", json={
        "message": "What is Python?",
        "conversation_id": "   ",
    })
    assert response.status_code == 422


def test_chat_rejects_message_exceeding_max_length(client):
    response = client.post("/api/ai/chat", json={
        "message": "a" * 3000,
        "conversation_id": "conv-1",
    })
    assert response.status_code == 422


from unittest.mock import patch


@patch("app.api.routers.ai.generate_ai_response_with_tools")
def test_chat_accepts_valid_request(mock_generate, client):
    mock_generate.return_value = "Here are the available Python books..."

    response = client.post("/api/ai/chat", json={
        "message": "What Python books are available?",
        "conversation_id": "conv-1",
    })

    assert response.status_code == 200

