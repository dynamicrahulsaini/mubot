import discord
from discord.flags import Intents
from discord.ext import commands
from bot.secrets import Secrets
from bot.commands import Test


class MyClient(discord.Client):
    intents: Intents = None
    secrets: Secrets = None
    bot: commands.Bot = None

    def __init__(self) -> None:
        self.intents = Intents.default()
        self.intents.message_content = True
        self.secrets = Secrets()
        super().__init__(intents=self.intents)
        self.bot = commands.Bot(command_prefix="!", intents=self.intents)

    async def on_ready(self):
        """initialization log"""
        await self.sync(guild=discord.Object)
        # print(f"Logged in as {self.user} ")

    async def on_message(self, message):
        """message listener"""
        print(f"message for {self.user}")

    @staticmethod
    async def runClient():
        client: MyClient = MyClient()
        await client.bot.add_cog(Test(client.bot))
        await client.bot.start(token=client.secrets.token)
