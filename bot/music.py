from datetime import datetime
import logging

from discord import FFmpegPCMAudio
from discord.ext import commands
import yt_dlp


class Music(commands.Cog):
    bot: commands.Bot = None
    voice_joined_timestamp: dict = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        logging.info(f"join command called by {ctx.author}")
        self.voice_joined_timestamp[ctx.author.id] = datetime.now()
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Joined {channel.name}")
        else:
            await ctx.send("You are not in a voice channel!")

    @commands.command()
    async def play(self, ctx, *args):
        logging.info(f"play command called by {ctx.author}")
        if ctx.voice_client is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()

        url = ":".join(args[0].split(":")[1:])

        ydl_opts = {"format": "bestaudio", "quiet": True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]

        if ctx.voice_client.is_playing():
            await ctx.send("Already playing audio!")
            return

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        audio_from_url = FFmpegPCMAudio(
            executable="ffmpeg", source=audio_url, **ffmpeg_options
        )

        ctx.voice_client.play(audio_from_url)
        await ctx.send(f"Playing audio from {url}")

    @commands.command()
    async def leave(self, ctx):
        logging.info(
            f"leave command called by {ctx.author}, was in vc for {datetime.now() - self.voice_joined_timestamp[ctx.author.id]}"
        )
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel!")
        else:
            await ctx.send("I'm not in a voice channel!")
