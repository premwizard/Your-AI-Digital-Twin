from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.db import mongo
import jwt, datetime
from app.core.config import Config

def register_user(request):
    data = request.get_json()
    user = mongo.db.users.find_one({"email": data["email"]})
    if user:
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(data["password"])
    new_user = {
        "username": data["username"],
        "email": data["email"],
        "password": hashed_pw,
        "role": "user",
        "createdAt": datetime.datetime.utcnow()
    }
    mongo.db.users.insert_one(new_user)
    return jsonify({"message": "Registered successfully"}), 201

def login_user(request):
    data = request.get_json()
    user = mongo.db.users.find_one({"email": data["email"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, Config.SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})
