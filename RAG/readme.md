RAG experiments

This folder contains Retrieval-Augmented Generation (RAG) experiments and small projects used to evaluate retrieval and reranking approaches.

Contents

- 01_youtube_rag/
  - A YouTube RAG pipeline that performs transcript-grounded retrieval and evaluates retrieval quality.
  - Evaluation notes: compared a FAISS semantic-search baseline against a cross-encoder reranker. On the provided evaluation set, reranking decreased Hit@1 from 40% to 20% and MRR from 0.70 to 0.60, while Hit@3 remained 100%.
  - Evaluation set: 20 questions broken down by type:
    - Direct factual: 5
    - Concept / explanation: 5
    - Paraphrased: 4
    - Specific detail: 3
    - Comparison / reasoning: 2
    - Negative / unsupported: 1

Notes

- See the project README at 01_youtube_rag/README.md for additional details and experimental artifacts.
- This file (readme.md) is intended as a discovery-level summary for the RAG folder.
