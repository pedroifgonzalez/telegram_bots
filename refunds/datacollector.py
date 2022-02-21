from typing import Any

from dotenv import dotenv_values
from telethon import TelegramClient, events
from utils import filter_travels, parse_refunds

settings = dotenv_values(".env")
api_id = int(settings.get("APP_API_ID") or 0)
api_hash = str(settings.get("APP_API_HASH"))
app_title = str(settings.get("APP_TITLE"))

if not(api_id and api_hash and app_title):
    raise Exception("Missing env variables")
client = TelegramClient(app_title, api_id=api_id, api_hash=api_hash)


@client.on(events.NewMessage)
async def my_event_handler(event: Any):
    if "Reintegros" in event.raw_text:
        travels = parse_refunds(event.raw_text)
        filtered_travels = filter_travels(
            travels, origin="La Habana", day_of_week="sáb"
        )
        print(filtered_travels)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
