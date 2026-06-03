import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-secret")
    REFRESH_SECRET_KEY = os.environ.get("REFRESH_SECRET_KEY", "your-refresh-secret")
    MONGO_URI = os.environ.get("DB_URI", "mongodb://localhost:27017/clone_me")
    MONGO_DBNAME = os.environ.get("DB_NAME", "clone_me")
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "phi")
    RATE_LIMIT_MAX_REQUESTS = int(os.environ.get("RATE_LIMIT_MAX_REQUESTS", "100"))
    RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", "60"))
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() in ["1", "true", "yes"]
