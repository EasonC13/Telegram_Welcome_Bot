import logging

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from core.config import (
    MONGODB_URL,
    MAX_CONNECTIONS_COUNT,
    MIN_CONNECTIONS_COUNT,
)
from .mongodb import db


async def connect_to_mongo():
    logging.info("Connecting to MongoDB...")
    # db.client = AsyncIOMotorClient(str(MONGODB_URL),
    #                                maxPoolSize=MAX_CONNECTIONS_COUNT,
    #                                minPoolSize=MIN_CONNECTIONS_COUNT)
    db.client = MongoClient(str(MONGODB_URL))
    logging.info("Connecting to MongoDB Success.")


async def close_mongo_connection():
    logging.info("Closing Connection from MongoDB...")
    db.client.close()
    logging.info("Closing Connection from MongoDB Success.")