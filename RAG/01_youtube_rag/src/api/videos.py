from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import asyncio

from src.loaders.youtube_loader import load_transcript
from src.splitters.splitter import split_documents
from src.rag_instance import rag


router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

class VideoIngestRequest(BaseModel):
    url: HttpUrl

class VideoIngestResponse(BaseModel):
    status: str
    url: str
    message: str

@router.post(
    "",
    response_model=VideoIngestResponse
)
async def ingest_video(request: VideoIngestRequest):

    try:
        # 1. Get YouTube URL
        url = str(request.url)

        # 2. Load transcript (running synchronous operation in threadpool if it blocks)
        transcript = await asyncio.to_thread(load_transcript, url)

        # 3. Split transcript into chunks
        documents = await asyncio.to_thread(split_documents, transcript)

        # 4. Update RAG knowledge base
        chunk_count = await rag.ingest_documents_async(documents)

        # 5. Return response
        return {
            "status": "success",
            "url": url,
            "message": (
                f"Video ingested successfully. "
                f"Created {chunk_count} chunks."
            )
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Video ingestion failed: {str(e)}"
        )