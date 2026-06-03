from typing import Dict
from bson import ObjectId


def build_personality_profile(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "personality_type": data.get("personality_type", "unspecified"),
        "communication_style": data.get("communication_style", "balanced"),
        "career_interests": data.get("career_interests", []),
        "goals": data.get("goals", []),
        "strengths": data.get("strengths", []),
        "weaknesses": data.get("weaknesses", []),
        "skills": data.get("skills", []),
        "preferences": data.get("preferences", {}),
        "updated_at": data.get("updated_at"),
    }
