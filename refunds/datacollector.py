import argparse
from typing import Any, Dict

from model import Travel
from notifypy import Notify
from settings import API_HASH, API_ID, APP_TITLE
from telethon import TelegramClient, events
from utils import filter_travels, parse_refunds

parser = argparse.ArgumentParser(prog="Data Collector")
for name in Travel.__fields__:
    parser.add_argument(f"-{name}")

client = TelegramClient(APP_TITLE, api_id=API_ID, api_hash=API_HASH)
filters: Dict[str, Any] = dict()


@client.on(events.NewMessage)
async def my_event_handler(event: Any):
    if event._chat.username == "apkviajandoinfo" and event.is_channel:
        travels = parse_refunds(event.raw_text)
        filtered_travels = filter_travels(travels, **filters)
        for travel in filtered_travels:
            notification = Notify(APP_TITLE, travel)
            notification.send()


def main():
    args = parser.parse_args()
    filters.update(**vars(args))
    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
