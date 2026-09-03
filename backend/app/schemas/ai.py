from sqlmodel import SQLModel
from pydantic import BaseModel, field_validator

MAX_MESSAGE_LENGTH = 2000
MAX_CONVERSATION_ID_LENGTH = 100

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("message must not be empty")
        if len(v) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"message must not exceed {MAX_MESSAGE_LENGTH} characters")
        return v

    
    @field_validator("conversation_id")
    @classmethod
    def conversation_id_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("conversation_id must not be empty")
        if len(v) > MAX_CONVERSATION_ID_LENGTH:
            raise ValueError(
                f"conversation_id must not exceed {MAX_CONVERSATION_ID_LENGTH} characters"
            )
        return v


class ChatResponse(BaseModel):
    response: str
    conversation_id: str