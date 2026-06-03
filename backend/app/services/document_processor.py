from typing import List, Dict
from datetime import datetime
from app.services.embeddings import get_embedding
from app.core.db import mongo
from app.models.document_chunk import build_document_chunk


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    chunks = []
    if len(text) <= chunk_size:
        return [text]
    
    step = chunk_size - overlap
    for i in range(0, len(text), step):
        chunk = text[i : i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks


def process_document_with_embeddings(user_id: str, document_id: str, document_content: str, metadata: Dict = None) -> int:
    chunks = chunk_text(document_content)
    chunk_count = 0
    
    for idx, chunk_text_content in enumerate(chunks):
        embedding = get_embedding(chunk_text_content)
        if embedding is None:
            continue
        
        chunk_obj = build_document_chunk(user_id, {
            "document_id": str(document_id),
            "chunk_index": idx,
            "chunk_text": chunk_text_content,
            "embedding": embedding,
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        })
        
        result = mongo.db.document_chunks.insert_one(chunk_obj)
        if result.inserted_id:
            chunk_count += 1
    
    return chunk_count


def delete_document_chunks(document_id: str) -> int:
    result = mongo.db.document_chunks.delete_many({"document_id": str(document_id)})
    return result.deleted_count
