from functools import wraps
from flask import request
import jwt
from app.core.config import Config
from app.utils.responses import api_response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return api_response(error="Missing or invalid Authorization header", status=401)

        token = auth_header.split(" ", 1)[1]
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return api_response(error="Token expired", status=401)
        except jwt.InvalidTokenError:
            return api_response(error="Invalid token", status=401)

        return f(data, *args, **kwargs)
    return decorated
