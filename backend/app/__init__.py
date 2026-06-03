from flask import Flask, jsonify
from flask_cors import CORS
from .core.db import mongo
from .auth.routes import auth_bp
from .clone.routes import clone_bp
from .memory.routes import memory_bp
from .training.routes import training_bp
from .interview.routes import interview_bp
from .future_self.routes import future_self_bp
from .analytics.routes import analytics_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object("app.core.config.Config")
    mongo.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(clone_bp, url_prefix="/api/clone")
    app.register_blueprint(memory_bp, url_prefix="/api/memory")
    app.register_blueprint(training_bp, url_prefix="/api/training")
    app.register_blueprint(interview_bp, url_prefix="/api/interview")
    app.register_blueprint(future_self_bp, url_prefix="/api/future-self")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": "Not found"}), 404

    return app
