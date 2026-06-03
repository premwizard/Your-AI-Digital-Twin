from flask import Blueprint
from app.middleware.jwt_required import token_required
from app.analytics.controller import get_overview

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/overview", methods=["GET"])
@token_required
def analytics_overview(current_user):
    return get_overview(current_user)
