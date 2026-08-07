from loaders.youtube_loader import load_transcript
from splitters.splitter import split_documents
from utils import clean_transcript


youtube_url = input("Enter YouTube URL: ")

text = load_transcript(youtube_url)

text = clean_transcript(text)

documents = split_documents(text)

print(f"\nTotal Chunks: {len(documents)}\n")


for i, doc in enumerate(documents[:3]):
    print(f"------ Chunk {i+1} ------")
    print(doc.page_content)
    print()