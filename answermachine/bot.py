import os
from pathlib import Path
from typing import Any
import asyncio

from dotenv import dotenv_values
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.updater import Updater
from telegram.update import Update

from answer_machine import client

settings = dotenv_values(str(Path(__file__).parent) + os.sep + ".env")

BOT_TOKEN = settings.get("BOT_TOKEN") or ""
WELCOME_MESSAGE = "Hello! Welcome to Answer Machine Bot. Please write\
\\help to see the commands available."

updater: Any = Updater(
    BOT_TOKEN,
    use_context=True,
)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(WELCOME_MESSAGE)


def help(update: Update, context: CallbackContext):
    pass


async def start_answer_machine():
    await client.start()
    await client.run_until_disconnected()


def run(update: Update, context: CallbackContext):
    asyncio.run(start_answer_machine())


def stop(update: Update, context: CallbackContext):
    client.disconnect()


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("run", run))


if __name__ == "__main__":
    updater.start_polling()
