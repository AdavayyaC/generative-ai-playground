# Text Splitters

Large Language Models (LLMs) work best when information is delivered in manageable pieces. Instead of processing an entire document at once, we split it into smaller chunks that are easier to embed, retrieve, and reason over.

Text splitting is one of the core preprocessing steps in Retrieval-Augmented Generation (RAG), document search, AI chatbots, and knowledge base applications.

---

## Why Split Text?

Large documents introduce a few common problems:

- Higher token consumption
- Slower processing
- Poor retrieval accuracy
- Lost context inside lengthy documents

Rather than treating a document as one giant block, text splitters divide it into smaller chunks while preserving as much context as possible.

```
Large Document
────────────────────────────────────────────

                 │
                 ▼

┌──────────────┐
│   Chunk 1    │
└──────────────┘

┌──────────────┐
│   Chunk 2    │
└──────────────┘

┌──────────────┐
│   Chunk 3    │
└──────────────┘

┌──────────────┐
│   Chunk 4    │
└──────────────┘
```

Each chunk can then be embedded, indexed, and retrieved independently.

---

# Core Concepts

## Chunk Size

`chunk_size` controls the maximum amount of text contained in each chunk.

| Smaller Chunks | Larger Chunks |
|---------------|---------------|
| Better retrieval precision | More surrounding context |
| Lower token usage | Higher token usage |
| Less context per chunk | Better for long passages |

There isn't a universal "best" value. The ideal chunk size depends on your documents and retrieval strategy.

---

## Chunk Overlap

Chunks don't always exist in isolation. Important information often spans across chunk boundaries.

Adding an overlap copies a small portion of one chunk into the next, helping preserve context.

Without overlap:

```
Chunk 1
The cat sat on the

Chunk 2
mat and looked outside.
```

With overlap:

```
Chunk 1
The cat sat on the mat.

Chunk 2
on the mat and looked outside.
```

> **Tip**
>
> A small overlap usually improves retrieval quality without significantly increasing token usage.

---

## Separators

A separator defines **where** text should be split.

Common separators include:

- Paragraphs (`\n\n`)
- New lines (`\n`)
- Spaces
- Sentences
- Custom delimiters

Using meaningful separators produces cleaner and more natural chunks.

---

# Splitter Types

## CharacterTextSplitter

Splits text using a single separator.

Use this when your documents already have predictable boundaries such as paragraphs, new lines, or custom delimiters.

**Good for**

- Plain text
- Structured files
- Custom separators

---

## RecursiveCharacterTextSplitter

The most commonly used splitter.

Instead of relying on a single separator, it recursively tries multiple separators until it creates chunks close to the desired size.

Typical order:

```
Paragraphs
    ↓
New Lines
    ↓
Sentences
    ↓
Words
    ↓
Characters
```

This approach preserves document structure better than simple character splitting.

**Recommended for**

- PDFs
- Articles
- Documentation
- Blogs
- General-purpose RAG

---

## Language-Aware Splitters

Source code isn't ordinary text.

Language-aware splitters understand programming language syntax and avoid splitting inside functions, classes, or code blocks whenever possible.

Supported languages include:

- Python
- JavaScript
- TypeScript
- Java
- HTML
- Markdown

Perfect for developer-focused AI applications.

---

# Comparison

| Splitter | Best Used For | Recommendation |
|-----------|---------------|----------------|
| CharacterTextSplitter | Plain text | Good |
| RecursiveCharacterTextSplitter | Documents & PDFs | ⭐ Recommended |
| Language-Aware Splitter | Source code | Best for code |

---

# Choosing the Right Splitter

| Content | Recommended Splitter |
|----------|----------------------|
| Text files | CharacterTextSplitter |
| PDFs | RecursiveCharacterTextSplitter |
| Documentation | RecursiveCharacterTextSplitter |
| Articles | RecursiveCharacterTextSplitter |
| Source code | Language-Aware Splitter |

---

# Configuration

Most splitters expose a few common parameters.

| Parameter | Description |
|-----------|-------------|
| `chunk_size` | Maximum size of each chunk |
| `chunk_overlap` | Shared text between neighboring chunks |
| `separator` | Character or pattern used to split text |
| `language` | Programming language used for code-aware splitting |

Example:

```python
chunk_size = 1000
chunk_overlap = 200
```

---

# Best Practices

✔ Start with `RecursiveCharacterTextSplitter` for most projects.

✔ Add a small overlap to preserve context.

✔ Keep chunks large enough to contain meaningful information.

✔ Use language-aware splitters when working with source code.

✔ Experiment with different chunk sizes—there's no one-size-fits-all configuration.

---

# Where You'll Use This

Text splitting powers many modern LLM applications, including:

- Retrieval-Augmented Generation (RAG)
- AI Chatbots
- PDF Question Answering
- Knowledge Bases
- Semantic Search
- Code Search
- Document Retrieval

Without chunking, retrieval systems become slower, less accurate, and more expensive.

---

# Project Files

| File | Description |
|------|-------------|
| `doc_splitter.py` | Recursive text splitting and language-aware examples |
| `length_based.py` | PDF loading with character-based chunking |
| `txt_structure_bsd.py` | Basic recursive chunking workflow |

---

# Next Steps

Try experimenting with the examples in this repository.

- Change the `chunk_size`
- Increase or decrease `chunk_overlap`
- Split your own PDFs
- Test different document types
- Compare retrieval quality with different settings

Small changes in chunking strategy can have a surprisingly large impact on the performance of your RAG pipeline.