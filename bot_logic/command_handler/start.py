import telegram
from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Dispatcher,
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    callbackcontext,
)

from db.mongodb import AsyncIOMotorClient, get_database, get_client

import asyncio
import nest_asyncio
from datetime import datetime

nest_asyncio.apply()


def start_handler_nonAwait(
    update: telegram.update.Update, context: callbackcontext.CallbackContext
):
    loop = asyncio.get_event_loop()

    loop.run_until_complete(start_handler(update, context))
    return "OK"


async def start_handler(
    update: telegram.update.Update, context: callbackcontext.CallbackContext
):
    print(update.message)
    user = context.bot.get_chat_member(
        chat_id=update.message.chat.id, user_id=update.message.from_user.id
    )['user']
    print(user)
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=Announcement,
        parse_mode="Markdown",
        # parse_mode="Markdown",
    )

    if update.message.chat.type == "private":
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="To use, please add this bot to a group.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Add GroupChatAdmin to group",
                            url="http://t.me/GroupChatAdminHelperBot?startgroup",
                        )
                    ]
                ]
            ),
        )
    # print(update.message.chat.type)
    return


Announcement = """
/setwelcomemsg {JSON}
add welcome message

in the following format:
`
[
    {
        "Type": "message",
        "parse_mode": "Markdown",
        "Notify": False,
        "Text": "# Hello World",
    },
    {
        "Type": "image",
        "Notify": False,
        "url": "https://i.imgur.com/GZnfN0w.gif",
    },
]
`

/testwelcomemsg
test the welcome message

"""
