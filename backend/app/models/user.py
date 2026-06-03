from app.core.db import mongo
from bson.objectid import ObjectId

def get_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})

def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def update_user_profile(user_id, update_data):
    return mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
