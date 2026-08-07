from langchain_community.vectorstores import FAISS


def create_vector_store(documents, embeddings):
    """
    Create a FAISS vector store from documents.
    """

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store


def save_vector_store(vector_store):
    """
    Save the vector database locally.
    """

    vector_store.save_local("data/vector_db")
    
    
def load_vector_store(embeddings):
    """
    Load the saved vector database.
    """

    vector_store = FAISS.load_local(
        "data/vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store