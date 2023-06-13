from fastapi import APIRouter, Request
import telegram
from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    callbackcontext,
)
from core.config import TELEGRAM_BOT_TOKEN

from db.mongodb import AsyncIOMotorClient, get_database, get_client
import json
import random

router = APIRouter()

from typing import Any, Dict, AnyStr, List, Union

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

using = {}


def new_memberNonAwait(update, context):
    loop = asyncio.get_event_loop()

    loop.run_until_complete(new_member(update, context))
    return "OK"


async def new_member(
    update: telegram.update.Update, context: callbackcontext.CallbackContext
):
    if using.get(update.message.chat.id, False):
        return
    using[update.message.chat.id] = True
    try:
        db = await get_database()
        col = db["groups"]
        print(col)
        group = col.find_one({"chat_id": update.message.chat.id})
        if group:
            pass
        else:
            col.insert_one(
                {
                    "chat_id": update.message.chat.id,
                    "prev_welcome_msg_ids": [],
                    "welcome": '[{"Type": "send_animation", "Notify": false, "url": "https://i.imgur.com/NMlXoNN.mp4"}]',
                }
            )
            group = col.find_one({"chat_id": update.message.chat.id})
        welcome_messages = json.loads(group["welcome"])
        res_msg_ids = []
        for welcome_message in welcome_messages:
            if welcome_message["Type"] == "send_animation":
                res = context.bot.send_animation(
                    update.message.chat.id, "https://i.imgur.com/NMlXoNN.mp4"
                )
                res_msg_ids.append(res.message_id)

        col.update_one(
            {"chat_id": update.message.chat.id},
            {
                "$push": {"prev_welcome_msg_ids": {"$each": res_msg_ids}},
            },
        )
        del_msg_ids = []
        for msg_id in group["prev_welcome_msg_ids"]:
            if res_msg_ids == msg_id:
                continue
            try:
                context.bot.delete_message(update.message.chat.id, msg_id)
                del_msg_ids.append(msg_id)
            except:
                pass
        col.update_one(
            {"chat_id": update.message.chat.id},
            {
                "$pull": {"prev_welcome_msg_ids": {"$in": del_msg_ids}},
            },
        )
    except:
        pass
    finally:
        using[update.message.chat.id] = False


from bot_logic.command_handler.start import start_handler_nonAwait

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher
# dispatcher.add_handler(CommandHandler("start", new_memberNonAwait))
# dispatcher.add_handler(CommandHandler("testwelcomemsg", start_handler_nonAwait))
# dispatcher.add_handler(CommandHandler("setwelcomemsg", start_handler_nonAwait))
dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, new_memberNonAwait)
)


from utils.doThreading import doThreading


import asyncio
import nest_asyncio

# nest_asyncio.apply()


def webhook_handler_nonAwait(arbitrary_json):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(webhook_handler(arbitrary_json))
    loop.close()
    return "OK"


async def webhook_handler(arbitrary_json):
    keys = list(arbitrary_json.keys())
    for key in keys:
        if type(key) == bytes:
            arbitrary_json[key.decode()] = arbitrary_json[key]
            del arbitrary_json[key]
    update = telegram.Update.de_json(arbitrary_json, bot)
    # doThreading(exec_common_operations_for_update_nonAwait, (update,))

    dispatcher.process_update(update)


@router.post("/webhook")
async def webhook(request: Request, arbitrary_json: JSONStructure = None):
    doThreading(webhook_handler_nonAwait, (arbitrary_json,))
    return "OK"
