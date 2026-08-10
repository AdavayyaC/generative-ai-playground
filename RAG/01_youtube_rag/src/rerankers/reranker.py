from sentence_transformers import CrossEncoder


def load_reranker():
    """
    Load the cross-encoder reranking model.
    """

    return CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )


def rerank_documents(
    question,
    documents,
    reranker,
    top_k=3
):
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