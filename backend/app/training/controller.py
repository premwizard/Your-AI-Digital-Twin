from datetime import datetime
from typing import Dict
from bson import ObjectId
from app.core.db import mongo
from app.models.training_document import build_training_document
from app.services.document_processor import process_document_with_embeddings, delete_document_chunks
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

    try:
        document_id = ObjectId(payload.get("document_id"))
    except Exception:
        return api_response(error="Invalid document_id", status=400)

    document = mongo.db.training_documents.find_one({"_id": document_id, "user_id": current_user["user_id"]})
    if not document:
        return api_response(error="Document not found", status=404)

    summary = document.get("content", "")[:1000]
    chunk_count = process_document_with_embeddings(
        current_user["user_id"],
        document_id,
        document.get("content", ""),
        metadata={
            "title": document.get("title"),
            "document_type": document.get("document_type"),
        },
    )

    mongo.db.training_documents.update_one(
        {"_id": document_id},
        {
            "$set": {
                "processed": True,
                "summary": summary,
                "chunk_count": chunk_count,
                "updated_at": datetime.utcnow(),
            }
        },
    )
    return api_response(message="Document processed with RAG", data={"document_id": str(document_id), "chunks_created": chunk_count})


def train_clone(current_user: Dict, payload: Dict):
    training_count = mongo.db.training_documents.count_documents({"user_id": current_user["user_id"], "processed": True})
    chunk_count = mongo.db.document_chunks.count_documents({"user_id": current_user["user_id"]})
    return api_response(message="Clone training initiated", data={"processed_documents": training_count, "total_chunks": chunk_count})


def delete_document(current_user: Dict, document_id: str):
    try:
        doc_id = ObjectId(document_id)
    except Exception:
        return api_response(error="Invalid document_id", status=400)

    document = mongo.db.training_documents.find_one({"_id": doc_id, "user_id": current_user["user_id"]})
    if not document:
        return api_response(error="Document not found", status=404)

    delete_document_chunks(document_id)
    mongo.db.training_documents.delete_one({"_id": doc_id})
    return api_response(message="Document deleted")


def list_documents(current_user: Dict):
    documents = list(mongo.db.training_documents.find({"user_id": current_user["user_id"]}).sort("created_at", -1))
    for document in documents:
        document["id"] = str(document.pop("_id"))
        document["content"] = document["content"][:200]
    return api_response(data=documents)
