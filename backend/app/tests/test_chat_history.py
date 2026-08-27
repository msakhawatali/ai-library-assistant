from app.services.chat_history import get_history, add_message, _conversations


def setup_function():
    _conversations.clear()


def test_add_and_get_history():
    add_message("conv1", "user", "Hello")
    add_message("conv1", "assistant", "Hi there!")

    history = get_history("conv1")
    assert len(history) == 2
    assert history[0].role == "user"
    assert history[0].content == "Hello"
    assert history[1].role == "assistant"


def test_get_history_returns_empty_for_unknown_conversation():
    assert get_history("nonexistent") == []


def test_history_is_isolated_per_conversation():
    add_message("conv1", "user", "Message A")
    add_message("conv2", "user", "Message B")

    assert len(get_history("conv1")) == 1
    assert len(get_history("conv2")) == 1