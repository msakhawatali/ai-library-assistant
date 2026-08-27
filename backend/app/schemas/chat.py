from sqlmodel import SQLModel
from typing import Literal


class ChatMessage(SQLModel):
    role: Literal["user", "assistant"]
    content: str


