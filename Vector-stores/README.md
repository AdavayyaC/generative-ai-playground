# Vector Store Architecture: ChromaDB vs FAISS

## 📌 Overview

This project demonstrates a **local Retrieval-Augmented Generation (RAG)** pipeline using **ChromaDB** and **FAISS** as vector stores, **HuggingFace embeddings** (`all-MiniLM-L6-v2`) for document embeddings, and **Groq LLM** (`llama-3.3-70b-versatile`) for response generation.

---

## 🏗️ RAG Workflow

```text
Documents
    │
    ▼
Chunking + Metadata
    │
    ▼
Embeddings (all-MiniLM-L6-v2)
    │
    ▼
ChromaDB / FAISS
    │
    ▼
Similarity Search
    │
    ▼
Groq LLM
    │
    ▼
Generated Answer
```

---

## ⚖️ ChromaDB vs FAISS

| Feature | ChromaDB | FAISS |
|----------|----------|--------|
| Type | Vector Database | Vector Search Library |
| CRUD | ✅ Native | ❌ Delete + Add |
| Persistence | ✅ Automatic | ❌ Manual (`save_local()`) |
| Metadata Filtering | ✅ Supported | ⚠ Limited |
| Performance | Fast | Extremely Fast |
| Best For | Development & Prototyping | Production & Large Datasets |

---

## ⚠️ Notes

- **FAISS** does not support direct updates. Delete the old document and add the updated one.
- Use **local HuggingFace embeddings** to avoid embedding API costs.
- Store your **`GROQ_API_KEY`** in a `.env` file (never hardcode secrets).
- Windows users may see HuggingFace symlink warnings—these are harmless.

---

## 🚀 Setup

### Install Dependencies

```bash
pip install langchain langchain-community langchain-huggingface \
langchain-groq chromadb faiss-cpu python-dotenv
```

### Configure

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

### Run

```bash
# ChromaDB Example
python chromaDB.py

# FAISS Example
python faiss_DB.py
```

---

## 📁 Project Structure

```text
├── chromaDB.py
├── faiss_DB.py
├── chroma_db/
├── faiss_index/
├── .env
├── requirements.txt
└── README.md
```

---

## 🎯 Summary

- **ChromaDB** offers a simple, database-like experience with automatic persistence and CRUD operations.
- **FAISS** provides high-speed similarity search for production-scale applications.
- Both implementations use **local embeddings** and **Groq LLM** to build an efficient, cost-effective RAG pipeline.