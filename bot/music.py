from datetime import datetime
import logging

from discord import FFmpegPCMAudio
from discord.ext import commands
import yt_dlp

from bot.music_utils.yt import extract_song_info as extract_youtube_info
from bot.music_utils.spotify import extract_track_info as extract_spotify_info, search_by_title


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
            try:
                await channel.connect()
            except Exception as e:
                logging.error(f"Error connecting to voice channel: {str(e)}")
                await ctx.send("❌ Error connecting to voice channel. Please try again.")
                return
            await ctx.send(f"Joined {channel.name}")
        else:
            await ctx.send("You are not in a voice channel!")

    @commands.command()
    async def play(self, ctx, *args):
        logging.info(f"play command called by {ctx.author}")
        if ctx.voice_client is None:
            if ctx.author.voice:
                self.voice_joined_timestamp[ctx.author.id] = datetime.now()
                channel = ctx.author.voice.channel
                try:
                    await channel.connect()
                except Exception as e:
                    logging.error(f"Error connecting to voice channel: {str(e)}")
                    await ctx.send("❌ Error connecting to voice channel. Please try again.")
                    return

        url = ":".join(args[0].split(":")[1:])

        if ctx.voice_client.is_playing():
            await ctx.send("Already playing audio!")
            return

        # Try YouTube first
        song_info = extract_youtube_info(url)
        
        # If YouTube fails, try Spotify
        if not song_info and 'spotify.com' in url:
            song_info = extract_spotify_info(url)
        
        # If direct URL fails, try searching Spotify by title
        if not song_info:
            try:
                # Try to get title from YouTube URL
                with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if info and 'title' in info:
                        song_info = search_by_title(info['title'])
            except Exception as e:
                logging.error(f"Error extracting title for Spotify search: {str(e)}")

        if not song_info:
            await ctx.send("❌ Could not extract audio from the provided URL. Please try a different URL or service.")
            return

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        try:
            audio_from_url = FFmpegPCMAudio(
                executable="ffmpeg", source=song_info['url'], **ffmpeg_options
            )

            ctx.voice_client.play(audio_from_url)
            source_info = f"from {song_info['source']}"
            if song_info['source'] == 'spotify':
                source_info += " (preview)"
            await ctx.send(f"🎵 Now playing: {song_info['title']} by {song_info['artist']} {source_info}")
        except Exception as e:
            logging.error(f"Error playing audio: {str(e)}")
            await ctx.send("❌ Error playing audio. Please try a different URL or service.")

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

    @commands.command()
    async def pause(self, ctx):
        logging.info(f"pause command called by {ctx.author}")
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused the audio!")
        else:
            await ctx.send("Nothing is playing right now!")

    @commands.command()
    async def resume(self, ctx):
        logging.info(f"resume command called by {ctx.author}")
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed the audio!")
        else:
            await ctx.send("Nothing is paused right now!")


if __name__ == "__main__":
    print("This module should not be run directly. Please run main.py instead.")
