import time

from src.embeddings.embedding_model import load_embedding_model
from src.vectorstores.faiss_store import (
    load_vector_store,
    create_vector_store,
    save_vector_store,
)
from src.retrievers.retriever import get_retriever
from src.chains.rag_chain import create_rag_chain
from src.observability.langfuse import get_langfuse_handler


class RAGApplication:

    def __init__(self):

        print("Loading RAG Application...\n")

        # Embedding model
        self.embeddings = load_embedding_model()

        # Load existing vector store
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

        # Langfuse
        self.langfuse_handler = get_langfuse_handler()

        print("RAG Application Loaded Successfully!\n")

    # INGESTION
    def ingest_documents(self, documents):
        """
        Replace the current knowledge base with new documents.

        This method is source-independent.

        Documents can come from:
        - YouTube
        - PDF
        - text files
        - web pages
        - APIs
        """

        # Create new vector store
        self.vector_store = create_vector_store(
            documents,
            self.embeddings
        )

        # Save new vector store
        save_vector_store(
            self.vector_store
        )

        # Rebuild retriever using the new vector store
        self.retriever = get_retriever(
            self.vector_store
        )

        # Rebuild RAG chain using the new retriever
        self.rag_chain = create_rag_chain(
            self.retriever
        )

        return len(documents)

    # RETRIEVAL
    def retrieve(self, question):
        """
        Retrieve relevant documents for a question.
        """

        documents = self.retriever.invoke(
            question
        )

        return documents

    # ASK
    def ask(self, question):
        """
        Run the complete RAG pipeline.

        Returns:
            dict containing:
            - question
            - answer
            - sources
            - latency
        """

        start_time = time.perf_counter()

        # Retrieve documents
        documents = self.retrieve(
            question
        )

        # Generate answer
        answer = self.rag_chain.invoke(
            question,
            config={
                "callbacks": [
                    self.langfuse_handler
                ],
                "metadata": {
                    "top_k": 3,
                    "application": "youtube-rag",
                    "version": "v1"
                }
            }
        )

        end_time = time.perf_counter()

        latency = end_time - start_time

        # Prepare sources
        sources = []

        for document in documents:

            sources.append({
                "content": document.page_content,
                "metadata": document.metadata
            })

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "latency": latency
        }

    # EVALUATION
    def evaluate(self, question):
        """
        Run the RAG application and return
        evaluation-friendly output.
        """

        return self.ask(question)