from typing import Dict

def build_clone_settings(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "language": data.get("language", "en"),
        "timezone": data.get("timezone", "UTC"),
        "response_style": data.get("response_style", "professional"),
        "privacy_level": data.get("privacy_level", "standard"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
