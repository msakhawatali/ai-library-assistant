from sqlmodel import SQLModel


class ChatMessage(SQLModel):
    role: str  
    content: str


