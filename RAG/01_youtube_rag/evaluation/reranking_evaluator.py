from src.rag_app import RAGApplication
from src.rerankers.reranker import (
    load_reranker,
    rerank_documents
)
from evaluation.dataset import evaluation_data


rag = RAGApplication()

print("\nLoading reranker...")

reranker = load_reranker()

print("Reranker loaded successfully!\n")


for item in evaluation_data:

    question = item["question"]

    print("=" * 60)
    print("Question:")
    print(question)

    # ---------------------------------
    # Stage 1: FAISS retrieval
    # ---------------------------------

    documents = rag.retriever.invoke(
        question
    )

    print("\nFAISS Retrieved Documents:")

    for i, document in enumerate(documents):

        print(
            f"Document {i + 1}: "
            f"{document.page_content[:150]}..."
        )

    # ---------------------------------
    # Stage 2: Reranking
    # ---------------------------------

    reranked_documents = rerank_documents(
        question=question,
        documents=documents,
        reranker=reranker,
        top_k=3
    )

    print("\nAfter Reranking:")

    for i, document in enumerate(
        reranked_documents
    ):

        print(
            f"Document {i + 1}: "
            f"{document.page_content[:200]}..."
        )

    print()