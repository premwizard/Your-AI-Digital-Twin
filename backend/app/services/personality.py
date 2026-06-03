from typing import Dict
from app.core.db import mongo


def load_personality_profile(user_id: str) -> Dict:
    return mongo.db.personality_profiles.find_one({"user_id": user_id}) or {}


def personality_brief(personality: Dict) -> str:
    if not personality:
        return "No personality profile is available for this user."

    skills = ", ".join(personality.get("skills", [])) or "unspecified"
    interests = ", ".join(personality.get("career_interests", [])) or "unspecified"
    goals = ", ".join(personality.get("goals", [])) or "unspecified"
    strengths = ", ".join(personality.get("strengths", [])) or "unspecified"
    weaknesses = ", ".join(personality.get("weaknesses", [])) or "unspecified"
    preferences = personality.get("preferences", {})
    preference_lines = ", ".join([f"{k}: {v}" for k, v in preferences.items()]) if preferences else "none"

    return (
        f"Personality Type: {personality.get('personality_type', 'unspecified')}\n"
        f"Communication Style: {personality.get('communication_style', 'balanced')}\n"
        f"Career Interests: {interests}\n"
        f"Goals: {goals}\n"
        f"Strengths: {strengths}\n"
        f"Weaknesses: {weaknesses}\n"
        f"Skills: {skills}\n"
        f"Preferences: {preference_lines}"
    )


def personality_tone(personality: Dict) -> str:
    style = personality.get("communication_style", "balanced")
    tone_map = {
        "professional": "Use a polished and concise tone.",
        "friendly": "Use a warm, approachable tone.",
        "direct": "Use a direct and confident tone.",
        "empathetic": "Use an empathetic and supportive tone.",
        "creative": "Use an imaginative and inspiring tone.",
    }
    return tone_map.get(style, "Use a natural and thoughtful tone.")
