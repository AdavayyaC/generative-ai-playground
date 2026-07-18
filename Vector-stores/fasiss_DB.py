import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

# Load environment variables from .env file
load_dotenv()

# 1. Setup Local Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Setup Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Create LangChain documents for IPL players
docs = [
    Document(
        page_content="Virat Kohli is one of the most successful and consistent batsmen in IPL history. Known for his aggressive batting style and fitness, he has led the Royal Challengers Bangalore in multiple seasons.",
        metadata={"team": "Royal Challengers Bangalore", "role": "Batsman"}
    ),
    Document(
        page_content="Rohit Sharma is the most successful captain in IPL history, leading Mumbai Indians to five titles. He's known for his calm demeanor and ability to play big innings under pressure.",
        metadata={"team": "Mumbai Indians", "role": "Batsman"}
    ),
    Document(
        page_content="MS Dhoni, famously known as Captain Cool, has led Chennai Super Kings to multiple IPL titles. His finishing skills, wicketkeeping, and leadership are legendary.",
        metadata={"team": "Chennai Super Kings", "role": "Wicketkeeper/Batsman"}
    ),
    Document(
        page_content="Jasprit Bumrah is considered one of the best fast bowlers in T20 cricket. Playing for Mumbai Indians, he is known for his yorkers and death-over expertise.",
        metadata={"team": "Mumbai Indians", "role": "Bowler"}
    ),
    Document(
        page_content="Ravindra Jadeja is a dynamic all-rounder who contributes with both bat and ball. Representing Chennai Super Kings, his quick fielding and match-winning performances make him a key player.",
        metadata={"team": "Chennai Super Kings", "role": "All-rounder"}
    )
]

# Assign explicit IDs for updating/deleting
docs_ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]

# 3. Initialize FAISS Vector Store
# We use from_texts to easily pass the explicit IDs alongside content and metadata
vector_store = FAISS.from_texts(
    texts=[doc.page_content for doc in docs],
    embedding=embeddings,
    metadatas=[doc.metadata for doc in docs],
    ids=docs_ids
)

print("--- Saving FAISS Index to Disk ---")
# FAISS saves as two files: index.faiss and index.pkl
vector_store.save_local("faiss_ipl_index")
print("Saved to './faiss_ipl_index' folder.")

print("\n--- Searching for Bowlers ---")
search_results = vector_store.similarity_search_with_relevance_scores(
    query="who among these are bowlers?",
    k=2
)
for doc, score in search_results:
    print(f"Score: {score:.4f} | Content: {doc.page_content[:60]}...")
    
print("\n--- Metadata Filtering (CSK Players) ---")
csk_results = vector_store.similarity_search(
    query="",
    filter={"team": "Chennai Super Kings"}
)
for doc in csk_results:
    print(f"Team: {doc.metadata['team']} | Player: {doc.page_content[:40]}...")

print("\n--- Updating Document ---")
updated_doc1 = Document(
    page_content="Virat Kohli, the former captain of RCB, holds the record for the most runs in IPL history.",
    metadata={"team": "Royal Challengers Bangalore", "role": "Batsman"}
)
# Update using the explicit ID
vector_store.update_document(document_id="doc1", document=updated_doc1)
print("Updated doc1 successfully.")

print("\n--- Deleting Document ---")
vector_store.delete(ids=["doc5"])
print("Deleted doc5 (Ravindra Jadeja) successfully.")

# ==========================================
# BONUS: Using Groq to answer a question (RAG)
# ==========================================
print("\n--- Asking Groq LLM a question based on the FAISS Vector Store ---")
query = "Who is the best bowler in the database and what is his specialty?"
retrieved_docs = vector_store.similarity_search(query, k=1)
context = retrieved_docs[0].page_content

prompt = f"""Based on the following context, answer the question.
Context: {context}
Question: {query}
Answer:"""

response = llm.invoke(prompt)
print(f"Groq Response: {response.content}")

# ==========================================
# HOW TO LOAD IT LATER (Uncomment to test)
# ==========================================
# print("\n--- Loading FAISS Index from Disk ---")
# loaded_vector_store = FAISS.load_local(
#     "faiss_ipl_index",
#     embeddings,
#     allow_dangerous_deserialization=True # Required by LangChain for loading pickle files
# )
# print("Loaded successfully! Document count:", len(loaded_vector_store.docstore._dict))