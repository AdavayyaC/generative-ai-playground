from src.rag_app import RAGApplication


rag_app = RAGApplication()

print("RAG Application Ready!\n")


while True:

    question = input(
        "Ask a question (type 'exit' to quit): "
    )

    if question.lower() == "exit":
        break
    
    docs =  rag_app.retrieve(question)
    print(docs)
    answer = rag_app.ask(question)

    print("\nAnswer:")
    print(answer)
    print()