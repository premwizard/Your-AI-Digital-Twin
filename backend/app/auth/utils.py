import jwt
import datetime
from flask import current_app
from app.core.config import Config

def generate_token(user, expires_in=3600):
    """
    Generate a JWT token for the given user.

    Args:
        user (dict): The user object containing at least `_id` and `role`.
        expires_in (int): Token expiration time in seconds (default: 1 hour).

    Returns:
        str: Encoded JWT token.
    """
    payload = {
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """
    Decode a JWT token.

    Args:
        token (str): JWT token.

    Returns:
        dict or None: Decoded payload if valid, otherwise None.
    """
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("Token expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None
