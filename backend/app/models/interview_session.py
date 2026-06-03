from typing import Dict

def build_interview_session(user_id: str, data: Dict) -> Dict:
    return {
        "user_id": user_id,
        "mode": data.get("mode", "hr"),
        "questions": data.get("questions", []),
        "answers": data.get("answers", []),
        "feedback": data.get("feedback", {}),
        "score": data.get("score", None),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
