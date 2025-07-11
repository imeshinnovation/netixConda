from motor.motor_asyncio import AsyncIOMotorClient
from config.security import MONGO_URI

conn = AsyncIOMotorClient(MONGO_URI).veemind

