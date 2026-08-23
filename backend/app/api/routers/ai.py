from fastapi import APIRouter, Depends
from app.services.ai_service import generate_ai_response, extract_search_filters
from app.schemas.ai import ChatRequest, ChatResponse
from app.services.ai_context import build_book_context
from app.db.database import get_session
from sqlmodel import Session


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
    ai_text = generate_ai_response(request.message, book_context=book_context)
    return ChatResponse(response=ai_text)