from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(text: str):
    """
    Split transcript into chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    documents = splitter.create_documents([text])

    return documents