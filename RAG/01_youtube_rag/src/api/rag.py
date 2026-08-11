from fastapi import APIRouter
from pydantic import BaseModel

from src.rag_instance import rag


router = APIRouter(
    prefix="",
    tags=["RAG"]
)


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: AskRequest):

    return rag.ask(
        request.question
    )