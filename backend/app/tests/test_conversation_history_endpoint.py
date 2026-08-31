from app.services.chat_history import add_message, _conversations


def setup_function():
    _conversations.clear()


def test_get_conversation_messages_returns_chronological_order(client):
    add_message("conv-endpoint-test", "user", "What Python books are available?")
    add_message("conv-endpoint-test", "assistant", "Here are the available Python books...")

    response = client.get("/api/ai/conversations/conv-endpoint-test/messages")

    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 2
    assert data["messages"][0]["role"] == "user"
    assert data["messages"][0]["content"] == "What Python books are available?"
    assert data["messages"][1]["role"] == "assistant"


def test_get_conversation_messages_returns_empty_list_for_unknown_conversation(client):
    response = client.get("/api/ai/conversations/nonexistent-conv/messages")

    assert response.status_code == 200
    assert response.json() == {"messages": []}


def test_get_conversation_messages_only_returns_matching_conversation(client):
    add_message("conv-a", "user", "Message A")
    add_message("conv-b", "user", "Message B")

    response = client.get("/api/ai/conversations/conv-a/messages")

    data = response.json()
    assert len(data["messages"]) == 1
    assert data["messages"][0]["content"] == "Message A"