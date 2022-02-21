from typing import Any

from dotenv import dotenv_values
from telethon import TelegramClient, events

from utils import filter_travels, parse_refunds

settings = dotenv_values(".env")
api_id = settings.get("APP_API_ID")
api_hash = settings.get("APP_API_HASH")

client = TelegramClient("anon", api_id=api_id, api_hash=api_hash)
answer_machine = False
refunds = False


@client.on(events.NewMessage)
async def my_event_handler(event: Any):
    # global answer_machine, refunds
    # if event.chat.is_self and event.raw_text == "start answer machine":
    #     answer_machine = True
    # if event.chat.is_self and event.raw_text == "stop answer machine":
    #     answer_machine = False
    # if answer_machine:
    #     message = "Lo siento. Pedro Iván puede que esté ocupado ahora mismo"
    #     await client.send_message(event.sender_id, message)
    
    if "Reintegros" in event.raw_text:
        travels = parse_refunds(event.raw_text)
        # travels = filter_travels(travels, origin="La Habana",
       	#     day_of_week="sab")
        print(travels)

if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
