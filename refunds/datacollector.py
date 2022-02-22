import os
from pathlib import Path
from typing import Any, Dict

from dotenv import dotenv_values
from telethon import TelegramClient, events
from utils import filter_travels, parse_refunds

settings = dotenv_values(str(Path(__file__).parent) + os.sep + ".env")
api_id = int(settings.get("APP_API_ID") or 0)
api_hash = str(settings.get("APP_API_HASH"))
app_title = str(settings.get("APP_TITLE", "datacollector"))

if not(api_id and api_hash and app_title):
    raise Exception("Missing env variables")
client = TelegramClient(app_title, api_id=api_id, api_hash=api_hash)


@client.on(events.NewMessage)
async def my_event_handler(event: Any):
    if event._chat.username == "apkviajandoinfo" and event.is_channel:
        travels = parse_refunds(event.raw_text)
        # Add filters here (check Travel class attributes)
        # origin="La Habana", day_of_week="sáb"
        filters: Dict[str, Any] = dict()
        filtered_travels = filter_travels(
            travels, **filters
        )
        print(filtered_travels)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
