from flask import Blueprint, request
from app.middleware.jwt_required import token_required
from app.memory.controller import add_memory, list_memories, get_memory
from app.utils.responses import api_response

memory_bp = Blueprint("memory", __name__)

@memory_bp.route("/", methods=["GET"])
@token_required
def memory_list(current_user):
    return list_memories(current_user)

@memory_bp.route("/", methods=["POST"])
@token_required
def memory_add(current_user):
    payload = request.get_json(silent=True)
    if not payload:
        return api_response(error="Memory payload is required", status=400)
    return add_memory(current_user, payload)

@memory_bp.route("/<string:memory_id>", methods=["GET"])
@token_required
def memory_get(current_user, memory_id):
    return get_memory(current_user, memory_id)
