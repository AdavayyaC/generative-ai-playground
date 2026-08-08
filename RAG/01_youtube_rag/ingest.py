from src.loaders.youtube_loader import (
    load_transcript,
    save_transcript
)

from src.utils import clean_transcript

from src.splitters.splitter import split_documents

from src.embeddings.embedding_model import (
    load_embedding_model
)

from src.vectorstores.faiss_store import (
    create_vector_store,
    save_vector_store
)



# 1. Get YouTube URL
youtube_url = input("Enter YouTube URL: ")


# 2. Load transcript

text = load_transcript(youtube_url)

# 3. Save original transcript
save_transcript(
    text,
    "data/transcript.txt"
)

print("Transcript saved successfully!")


# 4. Clean transcript
text = clean_transcript(text)

# 5. Split transcript


documents = split_documents(text)

print(f"Total Chunks: {len(documents)}")

# 6. Load embedding model
embeddings = load_embedding_model()

# 7. Create FAISS database
vector_store = create_vector_store(
    documents,
    embeddings
)


# 8. Save FAISS database

save_vector_store(vector_store)

print("\nVector database created successfully!")