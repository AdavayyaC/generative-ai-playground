from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# 1. Load document
loader = TextLoader("docs.txt", encoding="utf-8")
documents = loader.load()

# 2. Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

# 3. Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Vector store
vector_store = FAISS.from_documents(docs, embeddings)

# 5. Retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})


# 6. llm model define
llm = ChatGroq(
    model='llama-3.1-8b-instant'
)


# 7. Prompt (STRICT grounding)
prompt = PromptTemplate(
    template="Answer the question using ONLY the context below If the answer is not in the context, say I don't know.{context}\n{question}",
    input_variables=["context", "question"]
)


# 8. ✅ Proper LCEL RAG chain
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
)

# 9. Invoke (input is just the question string)
query = "What are the key takeaways from the document?"
response = rag_chain.invoke(query)

print("\nAnswer ----------------------->\n")
print(response.content)
