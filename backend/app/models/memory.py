from typing import Dict

def build_memory(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "title": data.get("title", "Memory Entry"),
        "category": data.get("category", "general"),
        "content": data.get("content", ""),
        "metadata": data.get("metadata", {}),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
