from fastapi import APIRouter
from db.mongodb import AsyncIOMotorClient, get_database, get_client

router = APIRouter()
from api.api_v1.endpoints.bot import router as bot_router

router.include_router(bot_router, prefix="/telegram")
