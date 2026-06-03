from datetime import datetime, timedelta
from typing import Dict

import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId

from app.core.db import mongo
from app.core.config import Config
from app.utils.responses import api_response


def get_user_by_email(email: str):
    return mongo.db.users.find_one({"email": email})


def get_user_by_id(user_id: str):
    try:
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None


def register_user(payload: Dict):
    if not payload:
        return api_response(error="Missing registration payload", status=400)

    existing = get_user_by_email(payload.get("email"))
    if existing:
        return api_response(error="User already exists", status=400)

    password = payload.get("password")
    if not password:
        return api_response(error="Password is required", status=400)

    user_document = {
        "username": payload.get("username", payload.get("email")),
        "email": payload.get("email"),
        "password": generate_password_hash(password),
        "role": payload.get("role", "user"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = mongo.db.users.insert_one(user_document)
    if not result.inserted_id:
        return api_response(error="Unable to create user", status=500)

    return api_response(message="Registered successfully", data={"user_id": str(result.inserted_id)}, status=201)


def create_access_token(payload: Dict, expires_delta: timedelta | None = None) -> str:
    payload_copy = payload.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    payload_copy.update({"exp": expire})
    return jwt.encode(payload_copy, Config.SECRET_KEY, algorithm="HS256")


def create_refresh_token(payload: Dict, expires_delta: timedelta | None = None) -> str:
    payload_copy = payload.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=30))
    payload_copy.update({"exp": expire})
    return jwt.encode(payload_copy, Config.REFRESH_SECRET_KEY, algorithm="HS256")


def login_user(payload: Dict):
    if not payload:
        return api_response(error="Missing login payload", status=400)

    user = get_user_by_email(payload.get("email"))
    if not user or not check_password_hash(user["password"], payload.get("password", "")):
        return api_response(error="Invalid credentials", status=401)

    access_token = create_access_token({"user_id": str(user["_id"]), "role": user.get("role", "user")})
    refresh_token = create_refresh_token({"user_id": str(user["_id"])})

    return api_response(
        message="Login successful",
        data={"access_token": access_token, "refresh_token": refresh_token, "user": {"id": str(user["_id"]), "email": user["email"], "role": user.get("role", "user")}},
    )


def refresh_token(refresh_token_value: str):
    try:
        decoded = jwt.decode(refresh_token_value, Config.REFRESH_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return api_response(error="Refresh token expired", status=401)
    except jwt.InvalidTokenError:
        return api_response(error="Invalid refresh token", status=401)

    access_token = create_access_token({"user_id": decoded["user_id"], "role": decoded.get("role", "user")})
    return api_response(message="Access token refreshed", data={"access_token": access_token})
