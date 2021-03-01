import asyncio
import re
import sys

from gecore.console.console_handler import ConsoleHandler, SESSION_STRINGS_SECTION
from gecore.requester import GetContactRequester
from gecore.utils import get_session_string


async def main():
    console_handler = ConsoleHandler(sys.argv[1:])
    parser = console_handler.config_parser

    while True:
        if len(parser[SESSION_STRINGS_SECTION]) == 0:
            print("У вас нет ни одной активной сессии.")
            pair = await get_session_string(*console_handler.credentials)
            if pair is None:
                print("Завершение работы.")
                exit(0)
            else:
                username, session_string = pair
                parser.set(SESSION_STRINGS_SECTION, username, session_string)
                console_handler.dump_session_file()

        while True:
            phone_number = input("Введите номер телефона (exit|выход - для выхода): ")
            if re.match('(exit|выход)', phone_number, re.IGNORECASE):
                print('Завершение работы.')
                exit(0)
            elif re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone_number, re.IGNORECASE):
                break
            else:
                print("Некорректный ввод.")

        requester = GetContactRequester(console_handler=console_handler,
                                        chats=console_handler.bots)
        await requester.run()
        response = await requester.request(phone_number)
        print(f'response = {response}\n')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
