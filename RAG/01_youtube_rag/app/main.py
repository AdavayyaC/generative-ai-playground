from fastapi import FastAPI

from src.api.system import router as system_router
from src.api.rag import router as rag_router
from src.api.videos import router as videos_router

app = FastAPI(
    title="YouTube RAG API",
    description="Retrieval-Augmented Generation API for YouTube videos",
    version="1.0.0"
)


app.include_router(system_router)
app.include_router(rag_router)
app.include_router(videos_router)

@app.get("/")
def root():
    return {
        "message": "YouTube RAG API is running"
    }