"""discord bot module"""

import asyncio
import logging
from client import MyClient
import discord


async def main():
    discord.utils.setup_logging(level=logging.INFO, root=True)
    await MyClient.runClient()


if __name__ == "__main__":
    asyncio.run(main())
