from langchain_text_splitters  import CharacterTextSplitter


text = """Text splitting is the process of breaking a long document into smaller, easier-to-handle parts. Instead of giving the entire document to an AI system all at once — which might be too much to process — text splitting helps divide the content into chunks of a manageable size.

These chunks are usually based on sentences, paragraphs, or character limits and sometimes include some overlap so the system doesn’t lose the meaning that flows from one part to the next."""


text_splitter = CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
    separator=''
)


result = text_splitter.split_text(text=text)

print(result)