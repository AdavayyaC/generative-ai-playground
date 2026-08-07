def get_retriever(vector_store):
    """
    Create a retriever from the vector store.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever