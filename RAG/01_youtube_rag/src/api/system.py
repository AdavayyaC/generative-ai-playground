from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["System"]
)


@router.get("/health")
def health_check():
    """
    Check whether the RAG API is running.
    """

    return {
        "status": "healthy",
        "service": "youtube-rag"
    }


@router.get("/info")
def system_info():
    """
    Return basic information about the RAG application.
    """

    return {
        "application": "youtube-rag",
        "version": "v1",
        "llm": "llama-3.3-70b-versatile",
        "retrieval_top_k": 3,
        "observability": "langfuse"
    }