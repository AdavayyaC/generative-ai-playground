from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter
)


def split_documents(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    splitter_type: str = "recursive"
):
    """
    Split transcript into chunks using the selected strategy.
    """

    if splitter_type == "recursive":

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    elif splitter_type == "character":

        splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    else:
        raise ValueError(
            f"Unknown splitter type: {splitter_type}"
        )

    documents = splitter.create_documents([text])

    return documents