from typing import List, Dict
from app.services.embeddings import get_embedding, cosine_similarity
from app.core.db import mongo


def retrieve_relevant_chunks(user_id: str, query: str, limit: int = 5, threshold: float = 0.3) -> List[Dict]:
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return []
    
    chunks = list(mongo.db.document_chunks.find({"user_id": user_id}))
    if not chunks:
        return []
    
    scored_chunks = []
    for chunk in chunks:
        chunk_embedding = chunk.get("embedding", [])
        if not chunk_embedding:
            continue
        
        similarity = cosine_similarity(query_embedding, chunk_embedding)
        if similarity >= threshold:
            scored_chunks.append({
                "chunk_text": chunk.get("chunk_text", ""),
                "similarity": similarity,
                "document_id": chunk.get("document_id", ""),
                "metadata": chunk.get("metadata", {}),
            })
    
    scored_chunks.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_chunks[:limit]


def retrieve_chunks_by_document(document_id: str, limit: int = 10) -> List[Dict]:
    chunks = list(mongo.db.document_chunks.find({"document_id": str(document_id)}).sort("chunk_index", 1).limit(limit))
    result = []
    for chunk in chunks:
        result.append({
            "chunk_index": chunk.get("chunk_index", 0),
            "chunk_text": chunk.get("chunk_text", ""),
            "metadata": chunk.get("metadata", {}),
        })
    return result
