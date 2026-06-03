from datetime import datetime
from typing import Dict, List
from bson import ObjectId
from app.core.db import mongo


def load_recent_memories(user_id: str, limit: int = 8) -> List[Dict]:
    memories = list(mongo.db.memories.find({"user_id": user_id}).sort("created_at", -1).limit(limit))
    for memory in memories:
        memory["id"] = str(memory.pop("_id"))
    return memories


def summarize_memories(memories: List[Dict], max_chars: int = 900) -> str:
    if not memories:
        return "No stored memories are available."

    lines = []
    for memory in memories[:6]:
        title = memory.get("title", "Memory")
        content = memory.get("content", "").replace("\n", " ")
        lines.append(f"{title}: {content}")

    summary = " | ".join(lines)
    return summary[:max_chars]


def load_conversation_history(user_id: str, limit: int = 5) -> List[Dict]:
    conversations = list(mongo.db.conversation_history.find({"user_id": user_id}).sort("created_at", -1).limit(limit))
    for conversation in conversations:
        conversation["id"] = str(conversation.pop("_id"))
    return conversations


def summarize_conversations(conversations: List[Dict], max_chars: int = 900) -> str:
    if not conversations:
        return "No prior conversations are available."

    lines = []
    for conv in conversations[:4]:
        messages = conv.get("messages", [])
        if messages:
            user_texts = [m.get("content", "") for m in messages if m.get("role") == "user"]
            assistant_texts = [m.get("content", "") for m in messages if m.get("role") == "assistant"]
            if user_texts and assistant_texts:
                lines.append(f"Q: {user_texts[-1][:120]} A: {assistant_texts[-1][:120]}")
            elif conv.get("summary"):
                lines.append(conv.get("summary")[:180])
    summary = " | ".join(lines)
    return summary[:max_chars]


def compact_text(text: str, max_chars: int = 1800) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 3] + "..."


def build_conversation_summary(user_prompt: str, reply_text: str, max_chars: int = 1200) -> str:
    summary_text = f"User asked: {user_prompt}. Clone replied: {reply_text}"
    return summary_text[:max_chars]
