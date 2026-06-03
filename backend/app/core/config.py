import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-secret")
    DB_URI = os.environ.get("DB_URI", "mongodb://localhost:27017")
    DB_NAME = os.environ.get("DB_NAME", "clone_me")  # <-- Add this line
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "phi")
