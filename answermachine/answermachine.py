import os
from pathlib import Path
from typing import Any

from dotenv import dotenv_values
from telethon import TelegramClient, events

settings = dotenv_values(str(Path(__file__).parent) + os.sep + ".env")
api_id = int(settings.get("APP_API_ID") or 0)
api_hash = str(settings.get("APP_API_HASH"))
app_title = str(settings.get("APP_TITLE"))
usernames = str(settings.get("USERNAMES")).split(",")

if not (api_id and api_hash and app_title):
    raise Exception("Missing env variables")
client = TelegramClient(app_title, api_id=api_id, api_hash=api_hash)

BASIC_TEMPLATE = "🤖: Hello there!\nSoon my master see this message, \
he will text you."


@client.on(events.NewMessage)
async def my_event_handler(event: Any):
    my_user = await client.get_me()
    my_user_status = my_user.to_dict().get("status")
    if 'UserStatusOnline' not in my_user_status.values():
        # do stuff
        print("You are offline")


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
