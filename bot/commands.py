import argparse
from discord import Guild
from discord.ext import commands


class Test(commands.Cog):
    bot: commands.Bot = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def shimt(self, ctx, *args):
        await ctx.send("helloo")
