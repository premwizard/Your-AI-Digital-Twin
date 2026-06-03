# Save user interactions with clone
from app.core.db import mongo
import datetime

def save_history(user_id, prompt, reply):
    mongo.db.history.insert_one({
        "user_id": user_id,
        "prompt": prompt,
        "reply": reply,
        "timestamp": datetime.datetime.utcnow()
    })
