from typing import Optional
from bson import ObjectId
from app.db.mongo import get_db

COLLECTION = "users"

async def get_user_by_email(email: str) -> Optional[dict]:
    db = get_db()
    return await db[COLLECTION].find_one({"email": email})

async def create_user(data: dict) -> dict:
    db = get_db()
    result = await db[COLLECTION].insert_one(data)
    data["_id"] = result.inserted_id
    return data

