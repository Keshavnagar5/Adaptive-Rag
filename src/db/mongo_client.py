"""
MongoDB client initialization.
"""

import os

from motor.motor_asyncio import AsyncIOMotorClient


# MongoDB connection
#
# Local development:
#   mongodb://localhost:27017
#
# Render:
#   Set MONGODB_URI in Render Environment Variables
MONGO_URL = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017",
)

DB_NAME = os.getenv(
    "MONGODB_DB_NAME",
    "adaptive_rag",
)

client = AsyncIOMotorClient(MONGO_URL)

db = client[DB_NAME]