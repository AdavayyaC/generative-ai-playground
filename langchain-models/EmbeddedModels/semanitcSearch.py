from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


# documents( k-base)
documents = [
    "Bengaluru is the capital of Karnataka",
    "Chennai is the capital of Tamil Nadu",
    "Mumbai is the financial capital of India",
    "Delhi is the capital of India",
    "Kolkata is known for its culture",
    "Bangolre is known as silicon city of India"
]

# query
query = "what is the capital of karnataka?"

doc_embedding = embedding.embed_documents(documents)
qurey_embedding = embedding.embed_query(query)

def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b))


# cosine similarity
scores = []
for i , doc_embeds in enumerate(doc_embedding):
    score = cosine_similarity(qurey_embedding,doc_embeds)
    scores.append((documents[i],score))
    
    
# 7 Sort by similarity
scores.sort(key=lambda x: x[1], reverse=True)

# 8️ Print results
for doc, score in scores:
    print(f"{score:.4f} → {doc}")
    
best_doc, best_score = scores[0]

print("Best match:")
print(f"{best_score:.4f} → {best_doc}")
