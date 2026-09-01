from fastapi import APIRouter, Depends, HTTPException, status
from app.services.ai_service import generate_ai_response, extract_search_filters, AIServiceError
from app.schemas.ai import ChatRequest, ChatResponse
from app.services.ai_context import build_book_context
from app.db.database import get_session
from sqlmodel import Session
from app.services.chat_history import get_history, add_message
from app.schemas.chat import ConversationHistoryResponse


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)):
    filters = extract_search_filters(request.message)

    book_context = build_book_context(
        session,
        title=filters.get("title"),
        author=filters.get("author"),
        category=filters.get("category"),
        year=filters.get("year"),
        available=filters.get("available"),
    )
    history = get_history(request.conversation_id)
    add_message(request.conversation_id, "user", request.message)
    try:
        ai_text = generate_ai_response(request.message, book_context=book_context, history=history)
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable. Please try again later.",
        )

    add_message(request.conversation_id, "assistant", ai_text)
    return ChatResponse(response=ai_text)

@router.get("/conversations/{conversation_id}/messages", response_model=ConversationHistoryResponse)
def get_conversation_messages(conversation_id: str):
    messages = get_history(conversation_id)
    return ConversationHistoryResponse(messages=messages)