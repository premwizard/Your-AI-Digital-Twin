from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import ollama
import sys
import os

# Ensure imports work when running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Custom imports
from app.auth.utils import generate_token, decode_token
from app.core.config import Config  # Make sure this has DB_URI and DB_NAME

app = Flask(__name__)
CORS(app)

# MongoDB setup
try:
    client = MongoClient(Config.DB_URI)
    db = client[Config.DB_NAME]
    users_collection = db["users"]
except Exception as e:
    print("MongoDB connection error:", e)
    users_collection = None

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Healthcare API"}), 200

@app.route('/login', methods=['POST'])
def login():
    if not users_collection:
        return jsonify({"error": "Database not initialized"}), 500

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = users_collection.find_one({"email": email, "password": password})

    if user:
        token = generate_token(user)
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "role": user.get("role", "user")
            }
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/profile', methods=['GET'])
def profile():
    if not users_collection:
        return jsonify({"error": "Database not initialized"}), 500

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    decoded = decode_token(token)

    if not decoded:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = users_collection.find_one({"_id": ObjectId(decoded["user_id"])})

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": str(user["_id"]),
        "email": user["email"],
        "role": user.get("role", "user")
    }), 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = ollama.chat(model='phi', messages=[
            {"role": "user", "content": prompt}
        ])
        return jsonify({"response": response['message']['content']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
