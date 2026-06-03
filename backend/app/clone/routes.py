from flask import Blueprint
from app.middleware.jwt_required import token_required
from .controller import respond, update_personality_profile, retrieve_personality_profile

clone_bp = Blueprint("clone", __name__)

@clone_bp.route("/respond", methods=["POST"])
@token_required
def clone_respond(current_user):
    return respond(current_user)

@clone_bp.route("/personality", methods=["GET"])
@token_required
def clone_personality_get(current_user):
    return retrieve_personality_profile(current_user)

@clone_bp.route("/personality", methods=["POST", "PUT"])
@token_required
def clone_personality_update(current_user):
    return update_personality_profile(current_user)
