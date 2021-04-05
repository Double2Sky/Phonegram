import logging
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from phonegram.requests.bot_chat import BotChat
from phonegram.config.session import SessionConfig


logging.basicConfig(format='[%(asctime)s] MESSAGE:\n%(message)s\n',
                    level=logging.WARNING)


class Requester:
    def __init__(self, session_config: SessionConfig, bots: dict):
        """
        :param session_config: object of SessionConfig
        :param bots: JSON settings of a list of bots
        """
        self._session_config = session_config
        self._bots = []
        self._clients = []
        self._bots_config = bots
        self._names_bots = list(bots.keys())

    async def run(self):
        """
        This method makes connection to the all sessions that specified in the session config file.
        Also method initializes a dictionary containing the names of bots and list of TelegramClient objects.
        """
        clients = []
        for user_id, session_string in self._session_config.session_strings:
            api_id = self._session_config.api_id
            api_hash = self._session_config.api_hash
            client = TelegramClient(StringSession(session_string), api_id, api_hash)

            try:
                # Make connection: if the session string is correct, connection will be made without logging
                await client.start(phone=lambda: input("Пожалуйста, введите ваш номер телефона: "),
                                   code_callback=lambda: input("Пожалуйста, введите полученный код подтверждения: "))
            except Exception:
                print(f'Для пользователя с {user_id = } session_string недействительна и будет удалена.',
                      file=sys.stderr)

                self._session_config.remove_session_string(user_id)
                continue

            # Make a list of clients
            clients.append(client)

            # Update the parser object: maybe new updates were occurred
            session_string = client.session.save()
            self._session_config.add_session_string(user_id, session_string)

        # Initialize the list of bots and make dump of the session config file
        for name in self._names_bots:
            bot_chat = BotChat(name, clients, self._bots_config[name])
            self._bots.append(bot_chat)
        self._clients = clients

    async def request(self, phone_number: str):
        """
        Make request to the bots and aggregate all responses to one.

        :param phone_number: the requested phone number
        :return: aggregated response in JSON format
        """
        result = {}
        tasks = []
        for bot in self._bots:
            tasks.append(bot.request(phone_number))

        for bot_name, bot_result in await asyncio.gather(*tasks, return_exceptions=True):
            result[bot_name] = bot_result

        return result

    async def stop(self):
        for client in self._clients:
            await client.disconnect()
