import asyncio
import re
from datetime import datetime, timedelta
from telethon import events


class BotChat:
    timeout = 60

    def __init__(self, name: str, clients: list):
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
        self.is_active = True
        self.response = None
        self.no_queries = False

    async def request(self, number):
        """

        :param number:
        :return:
        """
        for client in self.clients:
            await client.send_message(self.name, number)
            time = datetime.now()

            # response is None only if the message wasn't processed
            # not_queries is True if the client has no queries more to the bot
            while True:
                if self.response is not None or self.not_queries:
                    break
                await asyncio.sleep(0.1)

                # Check timeout time of answer
                if datetime.now() > time + timedelta(seconds=self.timeout):
                    return "Время ожидания ответа истекло"

            if self.response is not None:
                return self.response

        return "У вас нет запросов к этому боту"

    async def _handle_message(self, event):
        if re.search(r'запросов не осталось', event.text, re.IGNORECASE):
            self.not_queries = True
        elif re.search(r'(некорректный номер|настоящий getcontact|ничего не найдено)',
                       event.text, re.IGNORECASE):
            self.response = []
        elif event.is_reply and re.search('результаты', event.text, re.IGNORECASE):
            text = re.sub(r"Результаты по \+?[\d]{11}:", '', event.text)
            self.response = [name.strip() for name in text.split('\n') if name]
