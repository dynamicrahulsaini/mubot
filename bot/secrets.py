from os import path, getenv
from dotenv import dotenv_values
from discord import Client


class Secrets:
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
        if path.isfile(".env"):
            config: dict = dotenv_values(".env")
            self.token = config["DISCORD_TOKEN"]
            self.app_id = config["DISCORD_APP_ID"]
            self.public_key = config["DISCORD_PUBLIC_KEY"]
        else:
            self.token = getenv("DISCORD_TOKEN")
            self.app_id = getenv("DISCORD_APP_ID")
            self.public_key = getenv("DISCORD_PUBLIC_KEY")

    def run(self, client: Client):
        """run discord server client"""
        client.run(self.token)
