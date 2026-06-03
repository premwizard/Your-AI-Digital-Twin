from typing import Dict
from app.core.db import mongo


def load_future_profile(user_id: str) -> Dict:
    return mongo.db.future_profiles.find_one({"user_id": user_id}) or {}


def future_profile_brief(profile: Dict) -> str:
    if not profile:
        return "No future self profile is defined."

    career_goals = ", ".join(profile.get("career_goals", [])) or "unspecified"
    return (
        f"Target Role: {profile.get('target_role', 'unspecified')}\n"
        f"Timeline: {profile.get('timeline', 'unspecified')}\n"
        f"Career Goals: {career_goals}\n"
        f"Vision: {profile.get('vision', 'unspecified')}"
    )
