from datetime import datetime
from typing import Dict, List
from bson.objectid import ObjectId

from app.core.db import mongo
from app.models.personality_profile import build_personality_profile
from app.models.conversation_history import build_conversation_history
from app.services.llm import build_prompt, call_ollama
from app.rag.context_builder import assemble_context


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


def record_conversation(user_id: str, request_prompt: str, reply_text: str) -> None:
    conversation = build_conversation_history(user_id, {
        "conversation_type": "clone_chat",
        "messages": [{"role": "user", "content": request_prompt}, {"role": "assistant", "content": reply_text}],
        "summary": reply_text,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })
    mongo.db.conversation_history.insert_one(conversation)


def generate_clone_response(user_id: str, user_prompt: str) -> str:
    personality = get_personality_profile(user_id)
    memories = list(mongo.db.memories.find({"user_id": user_id}).sort("created_at", -1).limit(10))
    training_documents = list(mongo.db.training_documents.find({"user_id": user_id, "processed": True}).limit(5))
    context = assemble_context(personality, memories, training_documents)
    prompt = build_prompt(personality, memories, training_documents, user_prompt)
    answer = call_ollama(prompt, context=[{"role": "system", "content": context}])
    record_conversation(user_id, user_prompt, answer)
    return answer
