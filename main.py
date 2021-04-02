import asyncio
import sys
import json

from phonegram.console.console_handler import ConsoleHandler, SESSION_STRINGS_SECTION
from phonegram.requests.requester import GetContactRequester
from phonegram.utils import get_session_string


async def main():
    console_handler = ConsoleHandler(sys.argv[1:])
    parser = console_handler.config_parser

    if console_handler.mode == 'setting':
        while True:
            print(f'У вас активно {len(parser[SESSION_STRINGS_SECTION])} сессий на данный момент: ')
            for username, session_string in parser[SESSION_STRINGS_SECTION].items():
                print(username, '=', session_string)
            print()

            pair = await get_session_string(*console_handler.credentials)
            print()
            if pair is None:
                print("Завершение работы.")
                exit(0)
            else:
                username, session_string = pair
                parser.set(SESSION_STRINGS_SECTION, username, session_string)
                console_handler.dump_session_file()

    elif console_handler.mode == 'request':
        if len(parser[SESSION_STRINGS_SECTION]) == 0:
            print("У вас нет ни одной активной сессии. Настройте сессии в режиме setting.", file=sys.stderr)
            exit(-1)

        requester = GetContactRequester(console_handler=console_handler,
                                        bots=console_handler.bots)
        await requester.run()
        response = await requester.request(console_handler.phone_number)
        console_handler.to_out(json.dumps(response, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
