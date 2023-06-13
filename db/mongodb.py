from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.database import Database
from core.config import DATABASE_NAME

class DataBase:
    #client: AsyncIOMotorClient = None
    client: MongoClient = None
    


db = DataBase()


# async def get_client() -> AsyncIOMotorClient:
async def get_client() -> MongoClient:
    return db.client

# async def get_database() -> AsyncIOMotorDatabase:
async def get_database() -> Database:
    return db.client[DATABASE_NAME]

def get_database_noAwait() -> Database:
    return db.client[DATABASE_NAME]