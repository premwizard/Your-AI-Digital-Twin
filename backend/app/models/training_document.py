from typing import Dict

def build_training_document(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "document_type": data.get("document_type", "unknown"),
        "title": data.get("title", "Untitled Document"),
        "content": data.get("content", ""),
        "source": data.get("source", "upload"),
        "tags": data.get("tags", []),
        "processed": data.get("processed", False),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
