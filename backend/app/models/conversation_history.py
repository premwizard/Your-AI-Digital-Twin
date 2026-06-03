from typing import Dict

def build_conversation_history(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "conversation_type": data.get("conversation_type", "chat"),
        "messages": data.get("messages", []),
        "summary": data.get("summary", ""),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
