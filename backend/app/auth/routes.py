from flask import Blueprint, request
from .controller import register_user, login_user, refresh_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user(request)

@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user(request)

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    return refresh_access_token(request)
