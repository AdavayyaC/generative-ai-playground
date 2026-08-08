import time

from src.embeddings.embedding_model import load_embedding_model
from src.vectorstores.faiss_store import load_vector_store
from src.retrievers.retriever import get_retriever
from src.chains.rag_chain import create_rag_chain
from src.observability.langfuse import get_langfuse_handler

class RAGApplication:

    def __init__(self):

        # Load embedding model
        self.embeddings = load_embedding_model()

        # Load FAISS database
        self.vector_store = load_vector_store(
            self.embeddings
        )

        # Create retriever
        self.retriever = get_retriever(
            self.vector_store
        )

        # Create RAG chain
        self.rag_chain = create_rag_chain(
            self.retriever
        )
        
        # langfuse handler
        self.langfuse_handler = get_langfuse_handler()
        
    def retrieve(self, question):

        documents = self.retriever.invoke(question)

        return documents

    def ask(self, question):
        
        start_time = time.perf_counter()
        answer = self.rag_chain.invoke(
            question,
            config={
                "callbacks" : [self.langfuse_handler],
                "metadata" :{
                    "top_k" : 3,
                    "application" : "youtube-rag",
                    "version" : "v1"
                }
            }
        )

        end_time = time.perf_counter()

        latency = end_time - start_time

        return {
            "answer": answer,
            "latency": latency
        }
        

        
    def evaluate(self, question):

        documents = self.retrieve(question)

        answer = self.ask(question)

        return {
            "question": question,
            "answer": answer,
            "documents": documents
        }