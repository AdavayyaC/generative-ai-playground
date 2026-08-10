from src.rag_app import RAGApplication

rag = RAGApplication()

print("\nLoading transcript chunks...\n")

documents = rag.vector_store.docstore._dict

for index, (doc_id, document) in enumerate(documents.items()):

    print("=" * 80)

    print(f"Index: {index}")
    print(f"Document ID: {doc_id}")

    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)

    print()