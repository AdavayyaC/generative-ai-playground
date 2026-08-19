from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List, Any
from src.rerankers.reranker import CrossEncoderCompressor
from pydantic import Field, ConfigDict

class CustomContextualCompressionRetriever(BaseRetriever):
    base_retriever: BaseRetriever = Field(description="Base retriever to fetch initial documents")
    base_compressor: Any = Field(description="Compressor to rerank documents")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        docs = self.base_retriever.invoke(
            query, config={"callbacks": run_manager.get_child()}
        )
        if not docs:
            return []
            
        compressed_docs = self.base_compressor.compress_documents(
            docs, query, callbacks=run_manager.get_child()
        )
        return list(compressed_docs)

def get_retriever(vector_store, reranker_model=None):
    """
    Create a retriever from the vector store.
    If a reranker_model is provided, uses a contextual compression retriever.
    """
    
    # Base retriever fetches more documents initially
    base_retriever = vector_store.as_retriever(
        search_kwargs={"k": 10}
    )

    if reranker_model:
        compressor = CrossEncoderCompressor(
            reranker=reranker_model,
            top_k=3
        )
        retriever = CustomContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
        return retriever
        
    # Fallback to standard retriever if no reranker provided
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )
    
    return retriever