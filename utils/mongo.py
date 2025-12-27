from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
from .indexes import create_indexes

class MongoDB:
    client: AsyncIOMotorClient = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = mongodb.client[settings.MONGODB_DB_NAME]
    await create_indexes(db)
    print("✅ MongoDB connected")

async def close_mongo_connection():
    mongodb.client.close()
    print("🛑 MongoDB disconnected")

def get_database():
    return mongodb.client[settings.MONGODB_DB_NAME]
