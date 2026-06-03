from datetime import datetime
from app.core.db import mongo
from app.models.future_profile import build_future_profile
from app.services.llm import build_prompt, call_ollama
from app.utils.responses import api_response


def create_future_profile(current_user, payload):
    profile = build_future_profile(current_user["user_id"], payload)
    profile["created_at"] = datetime.utcnow()
    profile["updated_at"] = datetime.utcnow()
    existing = mongo.db.future_profiles.find_one({"user_id": current_user["user_id"]})
    if existing:
        mongo.db.future_profiles.update_one({"user_id": current_user["user_id"]}, {"$set": profile})
    else:
        mongo.db.future_profiles.insert_one(profile)
    return api_response(message="Future self profile saved", data=profile)


def get_future_profile(current_user):
    profile = mongo.db.future_profiles.find_one({"user_id": current_user["user_id"]}) or {}
    return api_response(data=profile)


def chat_future_self(current_user, payload):
    profile = mongo.db.future_profiles.find_one({"user_id": current_user["user_id"]})
    if not profile:
        return api_response(error="Future profile not defined", status=404)

    prompt = (
        f"You are the user's future self. Target role: {profile.get('target_role')}.",
        f"Timeline: {profile.get('timeline')}.",
        f"Career goals: {', '.join(profile.get('career_goals', []))}.",
        f"User asks: {payload['prompt']}"
    )

    answer = call_ollama("\n".join(prompt))
    return api_response(message="Future self response generated", data={"reply": answer})
