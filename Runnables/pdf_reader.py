from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Load document
loader = TextLoader("docs.txt", encoding="utf-8")
documents = loader.load()

# Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs = text_splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# FAISS vector store
vector_store = FAISS.from_documents(docs, embeddings)

# Retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Query : m
query = "What are the key takeaways from the document?"
retrieved_docs = retriever.invoke(query)

# combine retrived text into a single prompt
retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

# Print results
for i, doc in enumerate(retrieved_docs, 1):
    print(f"\n--- Document {i} ---")
    print(doc.page_content)

    
    
# llm model define
llm = ChatGroq(
    model='llama-3.1-8b-instant'
)

prompt = f"based on the following text, answer the question:{query}\n\n {retrieved_text}"

answer = llm.invoke(prompt)

# print the answer
print("Answer ----------------------->:\n", answer.content)
