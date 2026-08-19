from sentence_transformers import CrossEncoder
from typing import Sequence, Optional, Any
from langchain_core.documents import Document
from langchain_core.documents.compressor import BaseDocumentCompressor
from langchain_core.callbacks.manager import Callbacks
from pydantic import Field, ConfigDict

def load_reranker():
    """
    Load the cross-encoder reranking model.
    """
    return CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

def rerank_documents(
    question: str,
    documents: Sequence[Document],
    reranker: Any,
    top_k: int = 3
) -> Sequence[Document]:
    """
    Rerank retrieved documents based on
    question-document relevance.
    """
    pairs = [
        (question, document.page_content)
        for document in documents
    ]

    scores = reranker.predict(pairs)

    ranked_documents = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        document
        for document, score in ranked_documents[:top_k]
    ]

class CrossEncoderCompressor(BaseDocumentCompressor):
    """
    A DocumentCompressor that uses a CrossEncoder to rerank documents.
    """
    reranker: Any = Field(description="The loaded CrossEncoder model")
    top_k: int = Field(default=3, description="Number of documents to return after reranking")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        
        if not documents:
            return []
            
        return rerank_documents(
            question=query,
            documents=documents,
            reranker=self.reranker,
            top_k=self.top_k
        )