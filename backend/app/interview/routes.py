from flask import Blueprint, request
from app.middleware.jwt_required import token_required
from app.interview.controller import start_interview, list_sessions, get_feedback
from app.utils.responses import api_response

interview_bp = Blueprint("interview", __name__)

@interview_bp.route("/start", methods=["POST"])
@token_required
def interview_start(current_user):
    payload = request.get_json(silent=True)
    if not payload or not payload.get("mode"):
        return api_response(error="Interview mode is required", status=400)
    return start_interview(current_user, payload)

@interview_bp.route("/sessions", methods=["GET"])
@token_required
def interview_sessions(current_user):
    return list_sessions(current_user)

@interview_bp.route("/sessions/<string:session_id>/feedback", methods=["GET"])
@token_required
def interview_feedback(current_user, session_id):
    return get_feedback(current_user, session_id)
