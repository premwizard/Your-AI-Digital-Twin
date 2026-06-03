from datetime import datetime
from bson import ObjectId
from app.core.db import mongo
from app.models.interview_session import build_interview_session
from app.utils.responses import api_response


def start_interview(current_user, payload):
    session = build_interview_session(current_user["user_id"], payload)
    session["created_at"] = datetime.utcnow()
    session["updated_at"] = datetime.utcnow()
    result = mongo.db.interview_sessions.insert_one(session)
    if not result.inserted_id:
        return api_response(error="Unable to start interview session", status=500)
    return api_response(message="Interview session started", data={"session_id": str(result.inserted_id)})


def list_sessions(current_user):
    sessions = list(mongo.db.interview_sessions.find({"user_id": current_user["user_id"]}).sort("created_at", -1))
    for session in sessions:
        session["id"] = str(session.pop("_id"))
    return api_response(data=sessions)


def get_feedback(current_user, session_id):
    try:
        session = mongo.db.interview_sessions.find_one({"_id": ObjectId(session_id), "user_id": current_user["user_id"]})
    except Exception:
        session = None
    if not session:
        return api_response(error="Interview session not found", status=404)
    return api_response(data={"feedback": session.get("feedback", {}), "score": session.get("score")})
