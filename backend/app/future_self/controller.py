from datetime import datetime
from app.core.db import mongo
from app.models.future_profile import build_future_profile
from app.clone.service import generate_clone_response
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
    if not payload or not payload.get("prompt"):
        return api_response(error="Prompt is required", status=400)

    answer = generate_clone_response(current_user["user_id"], payload["prompt"], mode="future")
    return api_response(message="Future self response generated", data={"reply": answer})
