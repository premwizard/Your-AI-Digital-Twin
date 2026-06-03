from datetime import datetime
from typing import Dict, List
from bson import ObjectId

from app.core.db import mongo
from app.models.personality_profile import build_personality_profile
from app.models.conversation_history import build_conversation_history
from app.services.llm import call_ollama, build_brain_prompt
from app.services.personality import load_personality_profile
from app.services.memory import (
    load_recent_memories,
    load_conversation_history,
    summarize_conversations,
    build_conversation_summary,
)
from app.services.training import load_processed_documents
from app.services.future_self import load_future_profile
from app.services.context_builder import build_context


def save_personality_profile(user_id: str, payload: Dict) -> Dict:
    profile = build_personality_profile(user_id, payload)
    profile["updated_at"] = datetime.utcnow()
    existing = mongo.db.personality_profiles.find_one({"user_id": user_id})
    if existing:
        mongo.db.personality_profiles.update_one({"user_id": user_id}, {"$set": profile})
    else:
        profile["created_at"] = datetime.utcnow()
        mongo.db.personality_profiles.insert_one(profile)
    return profile


def get_personality_profile(user_id: str) -> Dict:
    return mongo.db.personality_profiles.find_one({"user_id": user_id}) or {}


def record_conversation(user_id: str, request_prompt: str, reply_text: str, mode: str) -> None:
    conversation = build_conversation_history(user_id, {
        "conversation_type": f"clone_{mode}",
        "messages": [
            {"role": "user", "content": request_prompt},
            {"role": "assistant", "content": reply_text},
        ],
        "summary": build_conversation_summary(request_prompt, reply_text),
        "metadata": {"mode": mode},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })
    mongo.db.conversation_history.insert_one(conversation)


def generate_clone_response(user_id: str, user_prompt: str, mode: str = "normal") -> str:
    personality = load_personality_profile(user_id)
    memories = load_recent_memories(user_id, limit=10)
    training_documents = load_processed_documents(user_id, limit=5)
    future_profile = load_future_profile(user_id)
    conversations = load_conversation_history(user_id, limit=4)
    conversation_summary = summarize_conversations(conversations)

    context = build_context(
        personality=personality,
        memories=memories,
        documents=training_documents,
        future_profile=future_profile,
        conversation_summary=conversation_summary,
        mode=mode,
        user_message=user_prompt,
    )

    prompt = build_brain_prompt(context, user_prompt)
    answer = call_ollama(prompt)
    record_conversation(user_id, user_prompt, answer, mode)
    return answer
