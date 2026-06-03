from flask import Blueprint, request, jsonify
from app.middleware.jwt_required import token_required
import subprocess
import json

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/respond', methods=['POST'])
@token_required
def respond(current_user):
    prompt = request.json.get("prompt")
    
    try:
        # Run Ollama model via command line
        process = subprocess.run(
            ["ollama", "run", "phi", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )

        if process.returncode != 0:
            return jsonify({"error": process.stderr.strip()}), 500
        
        output = process.stdout.strip()
        
        # Optional: clean response if Ollama adds system formatting
        return jsonify({"reply": output})
    
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ollama timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500
