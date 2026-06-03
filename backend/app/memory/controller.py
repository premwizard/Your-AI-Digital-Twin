from datetime import datetime
from bson import ObjectId
from app.core.db import mongo
from app.models.memory import build_memory
from app.utils.responses import api_response


def add_memory(current_user, payload):
    memory = build_memory(current_user["user_id"], payload)
    memory["created_at"] = datetime.utcnow()
    memory["updated_at"] = datetime.utcnow()
    result = mongo.db.memories.insert_one(memory)
    if not result.inserted_id:
        return api_response(error="Unable to save memory", status=500)
    return api_response(message="Memory created", data={"memory_id": str(result.inserted_id)})


def list_memories(current_user):
    memories = list(mongo.db.memories.find({"user_id": current_user["user_id"]}).sort("created_at", -1))
    for memory in memories:
        memory["id"] = str(memory.pop("_id"))
    return api_response(data=memories)


def get_memory(current_user, memory_id):
    try:
        memory = mongo.db.memories.find_one({"_id": ObjectId(memory_id), "user_id": current_user["user_id"]})
    except Exception:
        memory = None
    if not memory:
        return api_response(error="Memory not found", status=404)
    memory["id"] = str(memory.pop("_id"))
    return api_response(data=memory)
