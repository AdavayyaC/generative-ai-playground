from src.rag_app import RAGApplication
from evaluation.dataset import evaluation_data

from src.splitters.splitter import split_documents
from src.vectorstores.faiss_store import create_vector_store


# ============================================================
# Chunking Configurations
# ============================================================

CHUNKING_CONFIGS = [
    {
        "name": "Small",
        "chunk_size": 500,
        "chunk_overlap": 100,
    },
    {
        "name": "Baseline",
        "chunk_size": 1000,
        "chunk_overlap": 200,
    },
    {
        "name": "Large",
        "chunk_size": 1500,
        "chunk_overlap": 300,
    },
]


# ============================================================
# Metrics
# ============================================================

def calculate_cosine_similarity(vector1, vector2):
    """
    Calculate cosine similarity between two vectors.
    """

    dot_product = sum(
        a * b
        for a, b in zip(vector1, vector2)
    )

    magnitude1 = sum(
        a * a
        for a in vector1
    ) ** 0.5

    magnitude2 = sum(
        b * b
        for b in vector2
    ) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)


# ============================================================
# Relevance Check
# ============================================================

def is_relevant(document, keywords):
    """
    Determine whether a retrieved document contains
    at least one of the expected retrieval keywords.
    """

    content = document.page_content.lower()

    for keyword in keywords:

        if keyword.lower() in content:
            return True

    return False


# ============================================================
# Retrieval Evaluation
# ============================================================

def evaluate_retrieval(
    retriever,
    embeddings,
    evaluation_data,
    k_values=(1, 3),
):
    """
    Evaluate retrieval using:

    - Hit@K
    - MRR
    - Average Similarity
    """

    hit_counts = {
        k: 0
        for k in k_values
    }

    reciprocal_ranks = []

    all_similarities = []


    # --------------------------------------------------------
    # Evaluate every question
    # --------------------------------------------------------

    for item in evaluation_data:

        question = item["question"]

        retrieval_keywords = item[
            "retrieval_keywords"
        ]


        # ----------------------------------------------------
        # Retrieve documents
        # ----------------------------------------------------

        documents = retriever.invoke(
            question
        )


        # ----------------------------------------------------
        # Embed question
        # ----------------------------------------------------

        question_embedding = embeddings.embed_query(
            question
        )


        # ----------------------------------------------------
        # Calculate similarity
        # ----------------------------------------------------

        scored_documents = []

        for document in documents:

            document_embedding = embeddings.embed_query(
                document.page_content
            )

            similarity = calculate_cosine_similarity(
                question_embedding,
                document_embedding
            )

            scored_documents.append(
                (
                    document,
                    similarity
                )
            )

            all_similarities.append(
                similarity
            )


        # ----------------------------------------------------
        # Find relevant document rank
        # ----------------------------------------------------

        relevant_rank = None

        for rank, (document, score) in enumerate(
            scored_documents,
            start=1
        ):

            if is_relevant(
                document,
                retrieval_keywords
            ):

                relevant_rank = rank
                break


        # ----------------------------------------------------
        # Hit@K
        # ----------------------------------------------------

        for k in k_values:

            if (
                relevant_rank is not None
                and relevant_rank <= k
            ):
                hit_counts[k] += 1


        # ----------------------------------------------------
        # MRR
        # ----------------------------------------------------

        if relevant_rank is not None:

            reciprocal_ranks.append(
                1 / relevant_rank
            )

        else:

            reciprocal_ranks.append(0)


    # ========================================================
    # Final Metrics
    # ========================================================

    total_questions = len(
        evaluation_data
    )

    metrics = {}


    # --------------------------------------------------------
    # Hit@K
    # --------------------------------------------------------

    for k in k_values:

        metrics[f"hit@{k}"] = (
            hit_counts[k]
            / total_questions
        )


    # --------------------------------------------------------
    # Mean Reciprocal Rank
    # --------------------------------------------------------

    metrics["mrr"] = (
        sum(reciprocal_ranks)
        / total_questions
    )


    # --------------------------------------------------------
    # Average Similarity
    # --------------------------------------------------------

    metrics["average_similarity"] = (

        sum(all_similarities)
        / len(all_similarities)

        if all_similarities

        else 0
    )


    return metrics


# ============================================================
# Main
# ============================================================

print(
    "\nLoading RAG Application...\n"
)

rag = RAGApplication()

print(
    "RAG Application Loaded Successfully!"
)


# ============================================================
# Load Transcript
# ============================================================

with open(
    "data/transcript.txt",
    "r",
    encoding="utf-8"
) as file:

    transcript = file.read()


# ============================================================
# Run Chunking Experiments
# ============================================================

results = []


for config in CHUNKING_CONFIGS:

    print("\n" + "=" * 70)

    print(
        f"Chunking Configuration: "
        f"{config['name']}"
    )

    print(
        f"Chunk Size: "
        f"{config['chunk_size']}"
    )

    print(
        f"Chunk Overlap: "
        f"{config['chunk_overlap']}"
    )


    # --------------------------------------------------------
    # Create Chunks
    # --------------------------------------------------------

    documents = split_documents(
        transcript,
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"],
        splitter_type="recursive"
    )

    print(
        f"Total Chunks: "
        f"{len(documents)}"
    )


    # --------------------------------------------------------
    # Create Temporary Vector Store
    # --------------------------------------------------------

    vector_store = create_vector_store(
        documents,
        rag.embeddings
    )


    # --------------------------------------------------------
    # Create Retriever
    # --------------------------------------------------------

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 3
        }
    )


    # --------------------------------------------------------
    # Evaluate Retrieval
    # --------------------------------------------------------

    metrics = evaluate_retrieval(
        retriever,
        rag.embeddings,
        evaluation_data,
        k_values=(1, 3)
    )


    # --------------------------------------------------------
    # Display Results
    # --------------------------------------------------------

    print("\nRetrieval Results:")

    print(
        f"Hit@1 : "
        f"{metrics['hit@1']:.3f}"
    )

    print(
        f"Hit@3 : "
        f"{metrics['hit@3']:.3f}"
    )

    print(
        f"MRR   : "
        f"{metrics['mrr']:.3f}"
    )

    print(
        f"Average Similarity : "
        f"{metrics['average_similarity']:.4f}"
    )


    # --------------------------------------------------------
    # Store Results
    # --------------------------------------------------------

    results.append({

        "name": config["name"],

        "chunk_size":
            config["chunk_size"],

        "chunk_overlap":
            config["chunk_overlap"],

        "chunks":
            len(documents),

        **metrics
    })


# ============================================================
# Final Comparison
# ============================================================

print("\n")

print("=" * 70)

print(
    "FINAL CHUNKING COMPARISON"
)

print("=" * 70)


print(
    f"{'Config':<12}"
    f"{'Size':<8}"
    f"{'Overlap':<10}"
    f"{'Chunks':<8}"
    f"{'Hit@1':<10}"
    f"{'Hit@3':<10}"
    f"{'MRR':<10}"
    f"{'Avg Sim':<10}"
)

print("-" * 70)


for result in results:

    print(
        f"{result['name']:<12}"
        f"{result['chunk_size']:<8}"
        f"{result['chunk_overlap']:<10}"
        f"{result['chunks']:<8}"
        f"{result['hit@1']:<10.3f}"
        f"{result['hit@3']:<10.3f}"
        f"{result['mrr']:<10.3f}"
        f"{result['average_similarity']:<10.4f}"
    )


# Best Configuration

best = max(
    results,
    key=lambda x: x["mrr"]
)


print("\nBest Configuration:")

print(
    f"{best['name']} "
    f"(chunk_size="
    f"{best['chunk_size']}, "
    f"overlap="
    f"{best['chunk_overlap']})"
)

print(
    f"MRR: "
    f"{best['mrr']:.3f}"
)