# from loaders.youtube_loader import load_transcript
# from utils import clean_transcript
# from splitters.splitter import split_documents

# from embeddings.embedding_model import load_embedding_model
# from vectorstores.faiss_store import (
#     create_vector_store,
#     save_vector_store,
# )

# youtube_url = input("Enter YouTube URL: ")

# # Phase 1
# text = load_transcript(youtube_url)
# text = clean_transcript(text)
# documents = split_documents(text)

# print(f"Total Chunks: {len(documents)}")

# # Phase 2
# embeddings = load_embedding_model()

# vector_store = create_vector_store(
#     documents,
#     embeddings
# )

# save_vector_store(vector_store)

# print("\n✅ Vector database created successfully!")


from embeddings.embedding_model import load_embedding_model
from vectorstores.faiss_store import load_vector_store
from retrievers.retriever import get_retriever
from chains.rag_chain import create_rag_chain
embeddings = load_embedding_model()

vector_store = load_vector_store(embeddings)

retriever = get_retriever(vector_store)



print("Vector DB Loaded Successfully!\n")

print(vector_store.index.ntotal)

question = input("Ask a question: ")

documents = retriever.invoke(question)

print("\nRetrieved Documents:\n")

for i, doc in enumerate(documents):
    print(f"------ Document {i+1} ------")
    print(doc.page_content)
    print()
    
    
rag_chain = create_rag_chain(retriever)

while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    answer = rag_chain.invoke(question)

    print("\nAnswer:\n")
    print(answer)