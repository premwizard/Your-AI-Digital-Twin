from datetime import datetime
from typing import Dict
from app.core.db import mongo
from app.models.training_document import build_training_document
from app.utils.responses import api_response


def upload_document(current_user: Dict, payload: Dict):
    if not payload or not payload.get("content"):
        return api_response(error="Document content is required", status=400)

    document = build_training_document(current_user["user_id"], payload)
    document["created_at"] = datetime.utcnow()
    document["updated_at"] = datetime.utcnow()
    document["processed"] = False

    result = mongo.db.training_documents.insert_one(document)
    if not result.inserted_id:
        return api_response(error="Unable to save training document", status=500)
    return api_response(message="Document uploaded", data={"document_id": str(result.inserted_id)})


def process_document(current_user: Dict, payload: Dict):
    if not payload or not payload.get("document_id"):
        return api_response(error="document_id is required", status=400)

    document = mongo.db.training_documents.find_one({"_id": payload.get("document_id"), "user_id": current_user["user_id"]})
    if not document:
        return api_response(error="Document not found", status=404)

    summary = document.get("content", "")[:1000]
    mongo.db.training_documents.update_one({"_id": document["_id"]}, {"$set": {"processed": True, "summary": summary, "updated_at": datetime.utcnow()}})
    return api_response(message="Document processed", data={"document_id": str(document["_id"]), "summary": summary})


def train_clone(current_user: Dict, payload: Dict):
    training_count = mongo.db.training_documents.count_documents({"user_id": current_user["user_id"], "processed": True})
    return api_response(message="Clone training initiated", data={"processed_documents": training_count})
