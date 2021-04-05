import asyncio
import re
from datetime import datetime, timedelta
from telethon import events
<<<<<<< HEAD:phonegram/requests/bot_chat.py
from phonegram.utils import get_regex
=======
from phonegram.utils.utils import get_regex
>>>>>>> develop:gecore/requests/bot_chat.py
from telethon.errors.rpcerrorlist import UsernameInvalidError

# The defined parameters in the bots config file
FIELDS = "FIELDS"
NOT_FOUND = "NOT_FOUND"
NO_QUERIES = "NO_QUERIES"
ENABLED = "ENABLED"


class BotChat:
    timeout = 60

    def __init__(self, name: str, clients: list, bot_config: dict):
        """
        :param name:
        :param clients:
        """
        # Add event handler for each client
        for client in clients:
            client.add_event_handler(self._handle_message,
                                     events.NewMessage(chats=[name], incoming=True, outgoing=False))

        self.name = name
        self.clients = clients
        self.bot_config = bot_config
        self.is_active = True
        self.response = None
        self.no_queries = False

    async def request(self, number):
        """

        :param number:
        :return:
        """
        for client in self.clients:
            try:
                await client.send_message(self.name, number)
            except UsernameInvalidError:
                self.response = "Этот бот недоступен или не существует"

            time = datetime.now()

            # response is None only if the message wasn't processed
            # no_queries is True if the client has no queries more to the bot
            while True:
                if self.response is not None or self.no_queries:
                    break
                await asyncio.sleep(0.1)

                # Check timeout time of answer
                if datetime.now() > time + timedelta(seconds=self.timeout):
                    return self.name, "Время ожидания ответа истекло"

            if self.response is not None:
                return self.name, self.response

        return self.name, "У вас нет запросов к этому боту"

    async def _handle_message(self, event):
        no_queries_regex = get_regex(self.bot_config[NO_QUERIES]) \
            if NO_QUERIES in self.bot_config \
            else re.compile(r'запросов не осталось', re.IGNORECASE)

        not_found_regex = get_regex(self.bot_config[NOT_FOUND]) \
            if NOT_FOUND in self.bot_config \
            else re.compile(r'ничего не найдено', re.IGNORECASE)

        fields_regex = get_regex(self.bot_config[FIELDS]) \
            if FIELDS in self.bot_config \
            else re.compile(r'.*')

        if no_queries_regex.search(event.text):
            self.no_queries = True
        elif not_found_regex.search(event.text):
            self.response = "Ничего не найдено"
        elif fields_regex.search(event.text):
            text = re.sub(r"[^\w\s]", "", event.text)
            text = re.sub(r"\n+", "\n", text)
            text = re.sub(r" +", ' ', text)
            self.response = text
