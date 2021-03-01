class BotChat:
    def __init__(self, name: str, clients: list):
        """

        :param name:
        :param clients:
        """
        self.name = name
        self.clients = clients
        self.is_active = True
        self.response = None

    async def request(self, number):
        """

        :param number:
        :return:
        """
        await self.client.send_message(self.name, number)
