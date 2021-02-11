import asyncio
import sys
import logging
import re
from telethon import TelegramClient, events
from gecore.console_handler import ConsoleHandler
from telethon.events.common import EventCommon


logger = logging.getLogger('main')

SESSION_NAME = 'gecore'
BOT_NAME = 'getcontact_real_bot'


async def main():
    console_handler = ConsoleHandler(sys.argv[1:])
    api_id, api_hash = console_handler.credentials
    phone_number = console_handler.phone_number

    async with TelegramClient(SESSION_NAME, api_id, api_hash) as client:
        client.add_event_handler(handler, events.NewMessage(chats=[BOT_NAME], incoming=True, outgoing=False))
        await client.send_message(BOT_NAME, phone_number)
        await client.run_until_disconnected()


async def handler(event):
    print(event.text)
    if event.is_reply and re.search('результаты', event.text, re.IGNORECASE):
        text = re.sub(r"Результаты по \+?[\d]{11}", '', event.text)
        text

        await event.client.disconnect()
    elif re.search('некорректный номер', event.text, re.IGNORECASE):
        logger.error(event.text)
        await event.client.disconnect()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
