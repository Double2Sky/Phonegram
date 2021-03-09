import logging
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from gecore.console.console_handler import SESSION_STRINGS_SECTION, ConsoleHandler
from gecore.requests.bot_chat import BotChat

logging.basicConfig(format='[%(asctime)s] MESSAGE:\n%(message)s\n',
                    level=logging.WARNING)


class GetContactRequester:
    client: TelegramClient

    def __init__(self, console_handler: ConsoleHandler, chats: list):
        """
        :param chats: a list of chats that will be listened by this client
        :param console_handler: ConsoleHandler object
        """
        self._console_handler = console_handler
        self._bots = []
        self.chats = chats

    async def run(self):
        """
        This method makes connection to the all sessions that specified in the session config file.
        Also method initializes a dictionary containing the names of bots and list of TelegramClient objects.
        """
        clients = []
        parser = self._console_handler.config_parser
        for username, session_string in parser[SESSION_STRINGS_SECTION].items():
            client = TelegramClient(StringSession(session_string), *self._console_handler.credentials)

            try:
                # Make connection: if the session string is correct, connection will be made without logging
                await client.start(phone=lambda: input("Пожалуйста, введите ваш номер телефона: "),
                                   code_callback=lambda: input("Пожалуйста, введите полученный код подтверждения: "))
            except Exception:
                print(f'Для пользователя {username} session_string недействительна и будет удалена.', file=sys.stderr)
                parser.remove_option(SESSION_STRINGS_SECTION, username)
                continue

            # Make a list of clients
            clients.append(client)

            # Update the parser object: maybe new updates were occurred
            session_string = client.session.save()
            parser.set(SESSION_STRINGS_SECTION, username, session_string)

        # Initialize the list of bots and make dump of the session config file
        for chat in self.chats:
            bot_chat = BotChat(chat, clients)
            self._bots.append(bot_chat)
        self._console_handler.dump_session_file()

    async def request(self, phone_number: str):
        for chat in self.chats:
            await self.client.send_message(chat, phone_number)

        # response is None only if the message wasn't processed
        while True:
            if self.response is not None:
                break
            await asyncio.sleep(0.1)

        await self.client.disconnect()
        return self.response

    async def _start_client(self):
        self.response = None

        if not self.client.is_connected():
            await self.client.start()

    async def _handle_message(self, event):
        logging.warning(event.text)

        if re.search(r'(некорректный номер|запросов не осталось|настоящий getcontact|ничего не найдено)',
                     event.text, re.IGNORECASE):
            self.response = []
        elif event.is_reply and re.search('результаты', event.text, re.IGNORECASE):
            text = re.sub(r"Результаты по \+?[\d]{11}:", '', event.text)
            self.response = [name.strip() for name in text.split('\n') if name]
