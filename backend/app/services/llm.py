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


def build_prompt(personality: Dict, memories: List[Dict], documents: List[Dict], user_message: str) -> str:
    lines = ["You are an AI digital twin that must mirror the user's profile and memory."]
    if personality:
        lines.append("Personality and preferences:")
        lines.append(f"- Personality Type: {personality.get('personality_type')}")
        lines.append(f"- Communication Style: {personality.get('communication_style')}")
        lines.append(f"- Career Interests: {', '.join(personality.get('career_interests', []))}")
        lines.append(f"- Goals: {', '.join(personality.get('goals', []))}")
        lines.append(f"- Strengths: {', '.join(personality.get('strengths', []))}")
        lines.append(f"- Weaknesses: {', '.join(personality.get('weaknesses', []))}")
        lines.append(f"- Skills: {', '.join(personality.get('skills', []))}")
    if memories:
        lines.append("Relevant memories:")
        for memory in memories[:5]:
            lines.append(f"- {memory.get('title')}: {memory.get('content')}")
    if documents:
        lines.append("Training data summary:")
        for doc in documents[:3]:
            lines.append(f"- {doc.get('title', 'Document')}: {doc.get('content', '')[:120]}...")
    lines.append("Use this context to answer the user's request.")
    lines.append(f"User message: {user_message}")
    return "\n".join(lines)
