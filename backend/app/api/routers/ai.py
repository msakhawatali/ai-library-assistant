from fastapi import APIRouter, Depends, HTTPException, status
from app.services.ai_service import generate_ai_response_with_tools, AIServiceError
from app.schemas.ai import ChatRequest, ChatResponse
from app.db.database import get_session
from sqlmodel import Session
from app.services.chat_history import get_history, add_message
from app.schemas.chat import ConversationHistoryResponse


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)):
    history = get_history(request.conversation_id)
    add_message(request.conversation_id, "user", request.message)

    try:
        ai_text = generate_ai_response_with_tools(session, request.message, history=history)
    except AIServiceError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    add_message(request.conversation_id, "assistant", ai_text)
    return ChatResponse(response=ai_text, conversation_id=request.conversation_id)

@router.get("/conversations/{conversation_id}/messages", response_model=ConversationHistoryResponse)
def get_conversation_messages(conversation_id: str):
    messages = get_history(conversation_id)
    return ConversationHistoryResponse(messages=messages)