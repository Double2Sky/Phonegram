import asyncio
import sys
import json

from phonegram.console_handler import ConsoleHandler
from phonegram.requests.requester import Requester
from phonegram.utils.utils import get_session_string
from phonegram.config.session import SessionConfig


async def main():
    console_handler = ConsoleHandler(sys.argv[1:])
    session_config = SessionConfig.initialize(console_handler.credentials_filename)

    if console_handler.mode == 'setting':
        while True:
            print(f'У вас активно {len(session_config.session_strings)} сессий на данный момент: ')
            for user_id, session_string in session_config.session_strings:
                print(user_id, '=', session_string)
            print()

            pair = await get_session_string(api_id=session_config.api_id, api_hash=session_config.api_hash)
            print()
            if pair is None:
                print("Завершение работы.")
                exit(0)
            else:
                user_id, session_string = pair
                session_config.add_session_string(user_id, session_string)

    elif console_handler.mode == 'request':
        if len(session_config.session_strings) == 0:
            print("У вас нет ни одной активной сессии. Настройте сессии в режиме setting.", file=sys.stderr)
            exit(-1)

        requester = Requester(session_config=session_config, bots=console_handler.bots)
        await requester.run()
        response = await requester.request(console_handler.phone_number)
        await requester.stop()

        console_handler.to_out(json.dumps(response, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
