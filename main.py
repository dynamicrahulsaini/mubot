"""discord bot module"""
import os
import discord
from dotenv import dotenv_values

PERMISSION_INTEGER: int = 277028613440
intents = discord.Intents(PERMISSION_INTEGER)
intents.message_content = True

client = discord.Client(intents=intents)

class MuBot:
    """ 
        class providing the server client and config         
        properties:
            intents
            client
    """
    token: str = None
    app_id: str = None
    public_key: str = None

    def __init__(self) -> None:
        self.load_env()

    def load_env(self):
        """load environment variables"""
        if os.path.isfile('.env'):
            config: dict = dotenv_values('.env')
            self.token = config['DISCORD_TOKEN']
            self.app_id = config['APP_ID']
            self.public_key = config['PUBLIC_KEY']
        else:
            self.token = os.getenv('DISCORD_TOKEN')
            self.app_id = os.getenv('APP_ID')
            self.public_key = os.getenv('PUBLIC_KEY')

    def run(self):
        """run discord server client"""
        # if self.config['DISCORD_TOKEN']:
            # self.config['DISCORD_TOKEN'] = os.getenv('DISCORD_TOKEN')
        client.run(self.token)

    # @client.event
    @client.event
    async def on_ready(self):
        """initialization log"""
        print(f'Logged in as {client.user} ')

    @client.event
    async def on_message(self):
        """message listener"""
        print(f'message for {client.user}')

if __name__ == '__main__':
    mubot = MuBot()
    print(f'token: { mubot.token }')
    mubot.run()
