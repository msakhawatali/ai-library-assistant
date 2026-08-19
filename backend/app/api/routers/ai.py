from fastapi import APIRouter
from app.services.ai_service import generate_ai_response
from app.schemas.ai import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    ai_text = generate_ai_response(request.message)
    return ChatResponse(response=ai_text)