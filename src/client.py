from discord import Client
from discord.flags import Intents
from .secrets import Secrets


class MyClient(Client):
    intents: Intents = None
    secrets: Secrets = None

    def __init__(self, intents: Intents = None, secrets: Secrets = None) -> None:
        if intents:
            self.intents = intents
        else:
            self.intents = Intents.default()
            self.intents.message_content = True

        if secrets:
            self.secrets = secrets
        else:
            self.secrets = Secrets()

        super().__init__(intents=self.intents)

    async def on_ready(self):
        """initialization log"""
        print(f"Logged in as {self.user} ")

    async def on_message(self, message):
        """message listener"""
        print(f"message for {self.user}")

    @staticmethod
    def runClient():
        client: MyClient = MyClient()
        client.run(token=client.secrets.token)
