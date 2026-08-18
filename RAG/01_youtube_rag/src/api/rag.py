from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from src.rag_instance import rag


router = APIRouter(
    prefix="",
    tags=["RAG"]
)

class ChatMessage(BaseModel):
    role: str
    content: str

class AskRequest(BaseModel):
    question: str
    chat_history: Optional[List[ChatMessage]] = None

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]]
    latency: float

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):

    # Map simple chat history format to what Langchain expects if needed.
    history_dicts = None
    if request.chat_history is not None:
        history_dicts = [msg.model_dump() for msg in request.chat_history]
    
    return await rag.ask_async(
        question=request.question,
        chat_history=history_dicts
    )