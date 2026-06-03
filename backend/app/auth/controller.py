from flask import request
from .service import register_user as auth_register_user, login_user as auth_login_user, refresh_token as auth_refresh_token
from .schemas import validate_register_payload, validate_login_payload
from app.utils.responses import api_response


def register_user(request):
    payload = request.get_json(silent=True)
    errors = validate_register_payload(payload or {})
    if errors:
        return api_response(error=", ".join(errors), status=400)
    return auth_register_user(payload)


def login_user(request):
    payload = request.get_json(silent=True)
    errors = validate_login_payload(payload or {})
    if errors:
        return api_response(error=", ".join(errors), status=400)
    return auth_login_user(payload)


def refresh_access_token(request):
    payload = request.get_json(silent=True)
    if not payload or not payload.get("refresh_token"):
        return api_response(error="refresh_token is required", status=400)
    return auth_refresh_token(payload["refresh_token"])
