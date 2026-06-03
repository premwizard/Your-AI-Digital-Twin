from typing import Dict, List
from app.core.db import mongo


def load_processed_documents(user_id: str, limit: int = 5) -> List[Dict]:
    documents = list(mongo.db.training_documents.find({"user_id": user_id, "processed": True}).limit(limit))
    for document in documents:
        document["id"] = str(document.pop("_id"))
    return documents


def training_documents_brief(documents: List[Dict], max_chars: int = 1200) -> str:
    if not documents:
        return "No processed training documents are available."

    lines = []
    for document in documents[:4]:
        title = document.get("title", "Document")
        doc_type = document.get("document_type", "unknown")
        content = document.get("summary", document.get("content", "")).replace("\n", " ")
        lines.append(f"{title} ({doc_type}): {content[:200]}")

    return " | ".join(lines)[:max_chars]
