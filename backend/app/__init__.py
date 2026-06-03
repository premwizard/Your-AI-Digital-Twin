from flask import Flask
from flask_cors import CORS
from .core.db import mongo
from .auth.routes import auth_bp
from .chat.routes import chat_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object('app.core.config.Config')

    mongo.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(chat_bp, url_prefix="/api/clone")

    return app
