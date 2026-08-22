from fastapi import APIRouter, Depends
from app.services.ai_service import generate_ai_response
from app.schemas.ai import ChatRequest, ChatResponse
from app.services.ai_context import build_book_context
from app.db.database import get_session
from sqlmodel import Session


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)):
    book_context = build_book_context(session)
    ai_text = generate_ai_response(request.message, book_context=book_context)
    return ChatResponse(response=ai_text)