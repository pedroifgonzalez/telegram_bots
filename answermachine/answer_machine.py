import asyncio
from datetime import datetime
from typing import Any, Dict

from telethon import TelegramClient, events

from settings import API_HASH, API_ID, APP_TITLE, PHONE_NUMBERS, USERNAMES
from utils import UserStatus

client = TelegramClient(APP_TITLE, api_id=API_ID, api_hash=API_HASH)

ANSWER_MACHINE_MESSAGE = "🤖: Hello there! I'm just a bot\nSoon my master see\
this message, he will text you."


async def get_user_status_by_username(username: str) -> UserStatus:
    """
    Get a User Telegram status by given username

    :param username: User username to retrieve status from
    :type username: str
    :return: _description_
    :rtype: UserStatus
    """
    user_obj = await client.get_entity(username)
    user_dict: Dict[str, Any] = user_obj.to_dict()
    status: Dict[str, Any] = user_dict.get("status", {})
    name = status.get("_")
    was_online = status.get("was_online") or None
    expires_datetime = status.get("expires") or None
    user_status = UserStatus(
        name=name, was_online=was_online, expires_datetime=expires_datetime
    )
    return user_status


async def get_my_user_status() -> UserStatus:
    """
    Get my User Telegram status

    :return: A Telegram custom status
    :rtype: str
    """
    my_user = await client.get_me()
    my_user_status = await get_user_status_by_username(my_user.username)
    return my_user_status


async def check_offline_status_duration(duration: float) -> bool:
    """
    Check if user was offline during certain duration of time (seconds)

    :param duration: Duration given in seconds
    :type duration: float
    :return: Whether user was offline during that duration time or not
    :rtype: bool
    """
    user_status = await get_my_user_status()
    if user_status.name == "UserStatusOffline":
        start_datetime = datetime.now()
        await asyncio.sleep(duration)
        user_status = await get_my_user_status()
        end_datetime = datetime.now()
        difference_datetime = end_datetime - start_datetime
        if (
            user_status.name == "UserStatusOffline"
            and difference_datetime.seconds >= duration
        ):
            return True
    return False


@client.on(events.NewMessage)
async def handle_new_message(event: Any):
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
