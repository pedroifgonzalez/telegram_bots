import argparse
from datetime import datetime
from typing import Any, Dict

from notifypy import Notify
from telethon import TelegramClient, events

from model import Travel
from settings import API_HASH, API_ID, APP_TITLE
from utils import filter_travels, parse_refunds


class DateTimeAction(argparse.Action):
    """
    Custom Action for datetime argument

    :param argparse: argparse Action class
    :type argparse: class
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            values = datetime.fromisoformat(values)
            if values < datetime.today():
                raise ValueError("Set a datetime greater than today")
            setattr(namespace, self.dest, values)
        except ValueError:
            raise


parser = argparse.ArgumentParser(prog="Data Collector")
for name, atr in Travel.__fields__.items():
    if atr.type_ == datetime:
        parser.add_argument(f"-{name}", action=DateTimeAction)
        continue
    parser.add_argument(f"-{name}", type=atr.type_)

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
