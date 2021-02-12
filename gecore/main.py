import asyncio
import sys
from gecore.console_handler import ConsoleHandler
from gecore.requester import GetContactRequester


async def main():
    console_handler = ConsoleHandler(sys.argv[1:])
    phone_number = console_handler.phone_number

    requester = GetContactRequester(*console_handler.credentials, chats=['getcontact_real_bot'])
    response = await requester.request('getcontact_real_bot', phone_number)
    print('response =', response)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
