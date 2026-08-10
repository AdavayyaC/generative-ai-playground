from src.rag_app import RAGApplication
from evaluation.dataset import evaluation_data


def cosine_similarity(vector1, vector2):
    
    dot_product = sum(
        a * b
        for a, b in zip(vector1, vector2)
    )
    
    magnitude1 = sum(
        a*a 
        for a in vector1 
    ) ** 0.5
    
    magnitude2 = sum(
        b*b
        for b in vector2
    ) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    return dot_product / (magnitude1 * magnitude2)

def evaluate_k(rag, k):
    """
    Evaluate retrieval quality for a particular K.
    """

    print("\n" + "=" * 70)
    print(f"RETRIEVAL EVALUATION — K = {k}")
    print("=" * 70)

    hit_at_1 = 0
    hit_at_k = 0

    all_scores = []

    for item in evaluation_data:

        question = item["question"]

        print("\n" + "-" * 60)
        print(f"Question: {question}")

        # Retrieve more documents temporarily.
        # We will take only the first K.
        documents = rag.vector_store.similarity_search(
            question,
            k=k
        )

        question_embedding = rag.embeddings.embed_query(
            question
        )

        scores = []

        print("\nRetrieved Documents:")

        for i, document in enumerate(documents):

            document_embedding = rag.embeddings.embed_query(
                document.page_content
            )

            score = cosine_similarity(
                question_embedding,
                document_embedding
            )

            scores.append(score)
            all_scores.append(score)

            print(
                f"Document {i + 1} | "
                f"Score: {score:.4f}"
            )


        # Hit@1
        # For our current dataset, we use the ground-truth
        # answer terms to identify whether a relevant chunk
        # appears.
        #
        # This is a simple evaluation for learning purposes.
        # Later we can make this more rigorous.
        #
        ground_truth = item["ground_truth"].lower()

        relevant_found = False

        for document in documents:

            content = document.page_content.lower()

            # Basic semantic/content overlap check
            ground_truth_words = set(
                ground_truth.split()
            )

            content_words = set(
                content.split()
            )

            overlap = (
                len(ground_truth_words & content_words)
                / max(len(ground_truth_words), 1)
            )

            if overlap >= 0.15:
                relevant_found = True
                break

        if relevant_found:
            hit_at_k += 1

        # Hit@1
        if documents:

            first_content = documents[0].page_content.lower()

            ground_truth_words = set(
                ground_truth.split()
            )

            first_content_words = set(
                first_content.split()
            )

            overlap = (
                len(
                    ground_truth_words
                    & first_content_words
                )
                / max(len(ground_truth_words), 1)
            )

            if overlap >= 0.15:
                hit_at_1 += 1

    total_questions = len(evaluation_data)

    average_similarity = (
        sum(all_scores) / len(all_scores)
        if all_scores
        else 0
    )

    print("\n" + "=" * 70)
    print(f"K = {k} RESULTS")
    print("=" * 70)

    print(
        f"Hit@1: "
        f"{hit_at_1}/{total_questions}"
    )

    print(
        f"Hit@{k}: "
        f"{hit_at_k}/{total_questions}"
    )

    print(
        f"Average Similarity: "
        f"{average_similarity:.4f}"
    )


def main():

    print("\nLoading RAG Application...")

    rag = RAGApplication()

    print("\nRAG Application Loaded Successfully!")

    # Test different retrieval sizes
    k_values = [1, 3, 5, 7]

    for k in k_values:

        evaluate_k(
            rag,
            k
        )


if __name__ == "__main__":
    main()