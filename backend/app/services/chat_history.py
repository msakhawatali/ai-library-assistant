from app.schemas.chat import ChatMessage

_conversations: dict[str, list[ChatMessage]] = {}


def get_history(conversation_id: str) -> list[ChatMessage]:
    return _conversations.get(conversation_id, [])


def add_message(conversation_id: str, role: str, content: str) -> None:
    if conversation_id not in _conversations:
        _conversations[conversation_id] = []
    _conversations[conversation_id].append(ChatMessage(role=role, content=content))