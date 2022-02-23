import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from dotenv import dotenv_values
from telethon import TelegramClient, events

from utils import UserStatus

settings = dotenv_values(str(Path(__file__).parent) + os.sep + ".env")
api_id = int(settings.get("APP_API_ID") or 0)
api_hash = str(settings.get("APP_API_HASH"))
app_title = str(settings.get("APP_TITLE"))

if not (api_id and api_hash and app_title):
    raise Exception("Missing env variables")
client = TelegramClient(app_title, api_id=api_id, api_hash=api_hash)

USERNAMES = str(settings.get("USERNAMES")).split(",")
PHONE_NUMBERS = str(settings.get("PHONE_NUMBERS")).split(",")
ANSWER_MACHINE_MESSAGE = "🤖: Hello there! I'm just a bot\nSoon my master see\
this message, he will text you."


async def get_user_status() -> UserStatus:
    """
    Get User Telegram status

    :return: A Telegram custom status
    :rtype: str
    """
    my_user = await client.get_me()
    my_user_dict: Dict[str, Any] = my_user.to_dict()
    status: Dict[str, Any] = my_user_dict.get("status", {})
    name = status.get("_")
    was_online = status.get("was_online") or None
    expires_datetime = status.get("expires") or None
    my_user_status = UserStatus(
        name=name, was_online=was_online, expires_datetime=expires_datetime
    )
    return my_user_status


async def check_offline_status_duration(duration: float) -> bool:
    """
    Check if user was offline during certain duration of time (seconds)

    :param duration: Duration given in seconds
    :type duration: float
    :return: Whether user was offline during that duration time or not
    :rtype: bool
    """
    user_status = await get_user_status()
    if user_status.name == "UserStatusOffline":
        start_datetime = datetime.now()
        await asyncio.sleep(duration)
        user_status = await get_user_status()
        end_datetime = datetime.now()
        difference_datetime = end_datetime - start_datetime
        if (
            user_status.name == "UserStatusOffline"
            and difference_datetime.seconds >= duration
        ):
            return True
    return False


@client.on(events.NewMessage)
async def my_event_handler(event: Any):
    if event.is_private:
        if await check_offline_status_duration(10):
            sender = await event.get_sender()
            username = sender.username
            phone_number = sender.phone
            if username in USERNAMES or phone_number in PHONE_NUMBERS:
                await event.respond(ANSWER_MACHINE_MESSAGE)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
