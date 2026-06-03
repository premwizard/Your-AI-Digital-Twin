from app.core.db import mongo
from app.utils.responses import api_response


def get_overview(current_user):
    user_id = current_user["user_id"]
    data = {
        "total_conversations": mongo.db.conversation_history.count_documents({"user_id": user_id}),
        "memory_count": mongo.db.memories.count_documents({"user_id": user_id}),
        "training_documents_count": mongo.db.training_documents.count_documents({"user_id": user_id}),
        "interview_sessions": mongo.db.interview_sessions.count_documents({"user_id": user_id}),
        "future_profile_exists": bool(mongo.db.future_profiles.find_one({"user_id": user_id})),
    }
    return api_response(data=data)
