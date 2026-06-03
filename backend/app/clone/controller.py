from flask import request
from app.utils.responses import api_response
from app.clone.service import save_personality_profile, get_personality_profile, generate_clone_response


def update_personality_profile(current_user):
    payload = request.get_json(silent=True)
    if not payload:
        return api_response(error="Missing personality profile data", status=400)
    profile = save_personality_profile(current_user["user_id"], payload)
    return api_response(message="Personality profile saved", data=profile)


def retrieve_personality_profile(current_user):
    profile = get_personality_profile(current_user["user_id"])
    if not profile:
        return api_response(message="Personality profile not found", data={})
    return api_response(data=profile)


def respond(current_user):
    payload = request.get_json(silent=True)
    if not payload or not payload.get("prompt"):
        return api_response(error="Prompt is required", status=400)

    mode = payload.get("mode", "normal")
    answer = generate_clone_response(current_user["user_id"], payload["prompt"], mode=mode)
    return api_response(message="Response generated", data={"reply": answer})
