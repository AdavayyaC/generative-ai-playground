> "I tested reranking against a FAISS baseline. On my current evaluation set, it decreased Hit@1 from 40% to 20% and MRR from 0.70 to 0.60, while Hit@3 remained 100%."


20 questions

├── Direct factual          5
├── Concept / explanation   5
├── Paraphrased             4
├── Specific detail         3
├── Comparison / reasoning  2
└── Negative / unsupported  1




Built and evaluated a YouTube RAG pipeline with transcript-grounded retrieval evaluation, comparing FAISS semantic search against cross-encoder reranking using Hit@K and MRR metrics.  