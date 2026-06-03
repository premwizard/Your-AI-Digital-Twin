from typing import Dict

def build_future_profile(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "target_role": data.get("target_role", ""),
        "career_goals": data.get("career_goals", []),
        "timeline": data.get("timeline", ""),
        "vision": data.get("vision", ""),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
