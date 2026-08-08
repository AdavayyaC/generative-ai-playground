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

# Hit@K
def hit_at_k(documents, relevant_text, k):

    top_documents = documents[:k]

    for document in top_documents:

        if relevant_text.lower() in document.page_content.lower():
            return 1

    return 0



rag = RAGApplication()

print("\nRetrieval Evaluation Started\n")


for item in evaluation_data:

    question = item["question"]
    relevant_text = item["relevant_text"]

    print("=" * 60)
    print("Question:")
    print(question)

    # retrieved documents
    documents = rag.retrieve(question)

    # Convert question into embedding
    question_embedding = rag.embeddings.embed_query(
        question
    )

    print("\nRetrieved Documents:\n")

    scores = []

    for i, document in enumerate(documents):

        document_embedding = rag.embeddings.embed_query(
            document.page_content
        )

        score = cosine_similarity(
            question_embedding,
            document_embedding
        )

        scores.append(score)

        print(f"Document {i + 1}")
        print(f"Similarity Score: {score:.4f}")
        print(f"Content: {document.page_content[:200]}...")
        print()

    # Simliraity score
    if scores:
        average_score = sum(scores) / len(scores)
        best_score = max(scores)

        print(f"Best Score: {best_score:.4f}")
        print(f"Average Score: {average_score:.4f}")
        
    # Standard retrieval metric

    hit_1 = hit_at_k(
        documents,
        relevant_text,
        k=1
    )

    hit_3 = hit_at_k(
        documents,
        relevant_text,
        k=3
    )

    print(f"Hit@1: {hit_1}")
    print(f"Hit@3: {hit_3}")

    print()