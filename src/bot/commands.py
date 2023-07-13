from discord import Guild
from discord.ext import commands


@commands.Command
async def test(ctx):
    await ctx.send("shimt")


class Test(commands.Cog, name="test"):
    bot: commands.Bot = None

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        # self.client = client
        # self.bot.add_command(self.test)

    def te():
        return "h"

    @commands.command()
    async def test(ctx, args):
        await ctx.send("helloo")
