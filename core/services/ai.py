from sentence_transformers import SentenceTransformer
import os

# Global model instance (loaded lazily)
_model = None

def get_model():
    global _model
    if _model is None:
        # Downloads ~80MB model
        _model = SentenceTransformer('all-MiniLM-L6-v2') 
    return _model

def get_embedding(text: str):
    model = get_model()
    return model.encode(text).tolist()

# Mock Vector DB (In-memory for V1)
# In prod, this would be a Postgres table with vector column
vector_store = []

def add_to_index(doc_id: int, text: str):
    vec = get_embedding(text)
    vector_store.append({
        "id": doc_id,
        "text": text,
        "vector": vec
    })

def search_index(query: str, limit: int = 5):
    if not vector_store:
        return []
    
    query_vec = get_embedding(query)
    
    # Cosine Similarity (Manual implementation for no numpy dep if possible, but sentence-transformers uses torch/numpy)
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    
    vectors = [item["vector"] for item in vector_store]
    scores = cosine_similarity([query_vec], vectors)[0]
    
    # Zip and sort
    results = sorted(zip(scores, vector_store), key=lambda x: x[0], reverse=True)
    
    return [
        {"id": item["id"], "text": item["text"], "score": float(score)} 
        for score, item in results[:limit]
    ]
