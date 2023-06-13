from fastapi import FastAPI, Depends, status
import pymongo
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from core.errors import http_422_error_handler, http_error_handler
from db.mongodb import AsyncIOMotorClient, get_database
import asyncio

from datetime import datetime

from core.config import (
    ALLOWED_HOSTS,
    PROJECT_NAME,
    PROJECT_VERSION,
    API_PORT,
    DATABASE_NAME,
    API_V1_PREFIX,
    AUTH_V1_PREFIX,
)

app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from db.mongodb_connect import close_mongo_connection, connect_to_mongo

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)


from typing import Optional

from pydantic import BaseModel

from typing import Any, Dict, AnyStr, List, Union

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


from api.api_v1.router import router as api_router

app.include_router(api_router, prefix=API_V1_PREFIX)

import os


@app.on_event("startup")
async def start_watcher():
    os.system(
        f'''tmux new-session -c {os.getcwd()} -d -s _TON_Splitter_Bot_Watcher "python watcher.py"'''
    )


@app.on_event("shutdown")
async def stop_watcher():
    os.system("""tmux send-keys -t _TON_Splitter_Bot_Watcher C-c""")


if __name__ == "__main__":
    # import nest_asyncio
    # nest_asyncio.apply()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=13537)
