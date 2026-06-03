from typing import Dict, List, Optional


def build_document_chunk(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "document_id": data.get("document_id", ""),
        "chunk_index": data.get("chunk_index", 0),
        "chunk_text": data.get("chunk_text", ""),
        "embedding": data.get("embedding", []),
        "metadata": data.get("metadata", {}),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
