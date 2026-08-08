from src.rag_app import RAGApplication

from evaluation.dataset import evaluation_data

from evaluation.answer_evaluator import evaluate_answer

from evaluation.faithfulness_evaluator import (
    evaluate_faithfulness
)


rag = RAGApplication()


for item in evaluation_data:

    question = item["question"]

    ground_truth = item["ground_truth"]


    # -----------------------------
    # Retrieve documents
    # -----------------------------

    documents = rag.retrieve(question)


    # Combine retrieved documents
    # into one context string

    context = "\n\n".join(
        document.page_content
        for document in documents
    )


    # -----------------------------
    # Generate RAG answer
    # -----------------------------

    result = rag.ask(question)
    
    answer = result["answer"]
    latency = result["latency"]
    
    # -----------------------------
    # Evaluate correctness
    # -----------------------------

    correctness = evaluate_answer(
        question,
        ground_truth,
        answer
    )


    # -----------------------------
    # Evaluate faithfulness
    # -----------------------------

    faithfulness = evaluate_faithfulness(
        context,
        answer
    )


    # -----------------------------
    # Print results
    # -----------------------------

    print("\n" + "=" * 60)

    print("Question:")
    print(question)

    print("\nGround Truth:")
    print(ground_truth)

    print("\nRAG Answer:")
    print(answer)

    print("\nCorrectness:")
    print(correctness)

    print("\nFaithfulness:")
    print(faithfulness)
    
    print("\nLatency:")
    print(f"{latency:.2f} seconds")