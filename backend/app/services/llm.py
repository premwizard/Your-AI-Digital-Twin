from typing import Dict, List, Optional
import subprocess

try:
    import ollama
except ImportError:
    ollama = None

from app.core.config import Config
from app.utils.logger import logger


def call_ollama(prompt: str, context: Optional[List[Dict[str, str]]] = None) -> str:
    model_name = Config.OLLAMA_MODEL
    if ollama:
        try:
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": prompt})
            response = ollama.chat(model=model_name, messages=messages)
            if isinstance(response, dict):
                return response.get("message", {}).get("content", "")
            return str(response)
        except Exception as exc:
            logger.warning("Ollama Python client failed: %s", exc)

    try:
        args = ["ollama", "run", model_name, prompt]
        process = subprocess.run(args, capture_output=True, text=True, timeout=30)
        if process.returncode != 0:
            logger.error("Ollama subprocess error: %s", process.stderr.strip())
            raise RuntimeError(process.stderr.strip())
        return process.stdout.strip()
    except Exception as exc:
        logger.error("Ollama call failed: %s", exc)
        raise


def build_brain_prompt(context: str, user_message: str) -> str:
    prompt_parts = [
        "The text below contains the user's personality, memories, goals, documents, and recent conversations.",
        "Use this material to respond exactly like the user would, not like a generic assistant.",
        "If the user's preferences or experiences are mentioned, include them in the response in a natural way.",
        "Avoid generic AI phrasing such as 'As an AI' or 'I am a language model.'",
        "--- Context ---",
        context,
        "--- User Query ---",
        user_message,
        "--- Response Requirements ---",
        "- Answer in the user's voice.",
        "- Reference relevant memories and training documents when appropriate.",
        "- Keep the response personalized, concise, and practical.",
        "- Include career goals and future self perspective when applicable.",
    ]
    return "\n".join(prompt_parts)


def build_messages(context: str, user_message: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": context},
        {"role": "user", "content": user_message},
    ]
