from src.rag_app import RAGApplication
from evaluation.dataset import evaluation_data
from src.rerankers.reranker import rerank_documents, load_reranker


rag = RAGApplication()

print("Loading reranker...")
reranker = load_reranker()

print("\nRAG Application and Reranker loaded successfully!\n")

def evaluate_hit_at_k(documents, ground_truth_keywords, k):
    """
    Check whether a relevant document appears
    within the top-k retrieved documents.
    """

    top_documents = documents[:k]

    for document in top_documents:

        content = document.page_content.lower()

        if all(
            keyword.lower() in content
            for keyword in ground_truth_keywords
        ):
            return 1

    return 0


def reciprocal_rank(documents, ground_truth_keywords):
    """
    Calculate Reciprocal Rank.

    If relevant document is:
        position 1 -> 1.0
        position 2 -> 0.5
        position 3 -> 0.33
    """

    for index, document in enumerate(documents):

        content = document.page_content.lower()

        if all(
            keyword.lower() in content
            for keyword in ground_truth_keywords
        ):

            rank = index + 1

            return 1 / rank

    return 0


results = []


print("\n" + "=" * 70)
print("RETRIEVAL QUALITY COMPARISON")
print("=" * 70)


for item in evaluation_data:

    question = item["question"]

    # These keywords should come from the transcript
    # and represent the relevant chunk.
    keywords = item["retrieval_keywords"]

    print("\n" + "-" * 70)
    print("Question:")
    print(question)

    # ------------------------------------------------
    # 1. FAISS RETRIEVAL
    # ------------------------------------------------

    faiss_documents = rag.retrieve(question)

    # ------------------------------------------------
    # 2. RERANKING
    # ------------------------------------------------

    reranked_documents = rerank_documents(
        question,
        faiss_documents,
        reranker
    )

    # ------------------------------------------------
    # 3. METRICS
    # ------------------------------------------------

    faiss_hit_1 = evaluate_hit_at_k(
        faiss_documents,
        keywords,
        1
    )

    faiss_hit_3 = evaluate_hit_at_k(
        faiss_documents,
        keywords,
        3
    )

    faiss_mrr = reciprocal_rank(
        faiss_documents,
        keywords
    )

    reranked_hit_1 = evaluate_hit_at_k(
        reranked_documents,
        keywords,
        1
    )

    reranked_hit_3 = evaluate_hit_at_k(
        reranked_documents,
        keywords,
        3
    )

    reranked_mrr = reciprocal_rank(
        reranked_documents,
        keywords
    )

    # ------------------------------------------------
    # 4. DISPLAY
    # ------------------------------------------------

    print("\nFAISS:")

    print(f"Hit@1 : {faiss_hit_1}")
    print(f"Hit@3 : {faiss_hit_3}")
    print(f"MRR   : {faiss_mrr:.3f}")

    print("\nAfter Reranking:")

    print(f"Hit@1 : {reranked_hit_1}")
    print(f"Hit@3 : {reranked_hit_3}")
    print(f"MRR   : {reranked_mrr:.3f}")

    results.append({
        "question": question,

        "faiss_hit@1": faiss_hit_1,
        "faiss_hit@3": faiss_hit_3,
        "faiss_mrr": faiss_mrr,

        "reranked_hit@1": reranked_hit_1,
        "reranked_hit@3": reranked_hit_3,
        "reranked_mrr": reranked_mrr
    })


# ====================================================
# OVERALL RESULTS
# ====================================================

total = len(results)

faiss_hit_1 = sum(
    r["faiss_hit@1"]
    for r in results
)

faiss_hit_3 = sum(
    r["faiss_hit@3"]
    for r in results
)

reranked_hit_1 = sum(
    r["reranked_hit@1"]
    for r in results
)

reranked_hit_3 = sum(
    r["reranked_hit@3"]
    for r in results
)

faiss_mrr = sum(
    r["faiss_mrr"]
    for r in results
) / total

reranked_mrr = sum(
    r["reranked_mrr"]
    for r in results
) / total


print("\n" + "=" * 70)
print("OVERALL RESULTS")
print("=" * 70)

print(
    f"\nFAISS Hit@1: "
    f"{faiss_hit_1}/{total}"
)

print(
    f"Reranked Hit@1: "
    f"{reranked_hit_1}/{total}"
)

print(
    f"\nFAISS Hit@3: "
    f"{faiss_hit_3}/{total}"
)

print(
    f"Reranked Hit@3: "
    f"{reranked_hit_3}/{total}"
)

print(
    f"\nFAISS MRR: "
    f"{faiss_mrr:.3f}"
)

print(
    f"Reranked MRR: "
    f"{reranked_mrr:.3f}"
)

print("\n" + "=" * 70)