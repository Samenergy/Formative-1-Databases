import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_MONGO_NAME     = os.getenv("DB_MONGO_NAME")

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_MONGO_NAME]
