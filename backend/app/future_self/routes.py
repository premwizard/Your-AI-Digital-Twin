from flask import Blueprint, request
from app.middleware.jwt_required import token_required
from app.future_self.controller import create_future_profile, get_future_profile, chat_future_self
from app.utils.responses import api_response

future_self_bp = Blueprint("future_self", __name__)

@future_self_bp.route("/profile", methods=["POST"])
@token_required
def future_profile_create(current_user):
    payload = request.get_json(silent=True)
    if not payload:
        return api_response(error="Future profile payload is required", status=400)
    return create_future_profile(current_user, payload)

@future_self_bp.route("/profile", methods=["GET"])
@token_required
def future_profile_get(current_user):
    return get_future_profile(current_user)

@future_self_bp.route("/chat", methods=["POST"])
@token_required
def future_self_chat(current_user):
    payload = request.get_json(silent=True)
    if not payload or not payload.get("prompt"):
        return api_response(error="Prompt is required", status=400)
    return chat_future_self(current_user, payload)
