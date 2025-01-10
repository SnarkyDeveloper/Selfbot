import discord
import asyncio
import os
import yt_dlp
import glob
from discord.ext import commands
from ytmusicapi import YTMusic
from Backend.send import send

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ytmusic = YTMusic()
        self.queue = []
        self.loop = False
        self.skip = False
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../audio')
        os.makedirs(self.audio_dir, exist_ok=True)

    async def search_yt(self, query):
        try:
            search_results = self.ytmusic.search(query)
            if not search_results:
                return None, "No results found."
            video_id = search_results[0]['videoId']
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info, None
        except Exception as e:
            return None, str(e)

    async def download_song(self, query):
        try:
            info, error = await self.search_yt(query)
            if error:
                return None, error, None

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self.audio_dir, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"
                if not os.path.exists(filename):
                    ydl.download([info['webpage_url']])
            self.clean_old_files()
            return info, None, filename
        except Exception as e:
            return None, str(e), None

    def clean_old_files(self, max_files=30):
        """Delete the oldest files if the directory exceeds max_files."""
        audio_files = glob.glob(os.path.join(self.audio_dir, '*.mp3'))
        while len(audio_files) > max_files:
            oldest_file = min(audio_files, key=os.path.getctime)
            os.remove(oldest_file)
            audio_files = glob.glob(os.path.join(self.audio_dir, '*.mp3'))

    async def connect_to_voice(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            user = ctx.author
            if user.voice and user.voice.channel:
                for vc in self.bot.voice_clients:
                    if vc.guild == user.voice.channel.guild:
                        await vc.disconnect(force=True)
                return await user.voice.channel.connect()
            else:
                await send(self.bot, ctx, title="Error", content="You need to be in a voice channel!", color=0xFF0000)
                return None
        else:
            if ctx.author.voice and ctx.author.voice.channel:
                for vc in self.bot.voice_clients:
                    if vc.guild == ctx.guild:
                        await vc.disconnect(force=True)
                return await ctx.author.voice.channel.connect()
            else:
                await send(self.bot, ctx, title="Error", content="You need to be in a voice channel!", color=0xFF0000)
                return None

    @commands.command(description="Play a song")
    async def play(self, ctx, query):
        voice_client = await self.connect_to_voice(ctx)
        if not voice_client:
            return

        await send(self.bot, ctx, title="🔍 Searching", content=f"Searching for: {query}", color=0xFEE75C)
        info, error, filename = await self.download_song(query)
        if error:
            await send(self.bot, ctx, title="Error", content=f"Error: {error}", color=0xFF0000)
            await voice_client.disconnect()
            return

        name = info['title']
        author = info['uploader']
        await send(self.bot, ctx, title="Now Playing", content=f"🎵 Playing {name} by {author}", color=0x2ECC71)
        
        ffmpeg_options = {
            'options': '-vn -b:a 128k -bufsize 64k -ar 48000 -filter:a "loudnorm, volume=2.0"',
        }
        audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)
        voice_client.play(audio_source, after=lambda _: asyncio.run_coroutine_threadsafe(self.play_next(ctx, voice_client), self.bot.loop))
        self.queue.append((filename, name, author))

    async def play_next(self, ctx, voice_client):
        if voice_client and voice_client.is_connected():
            if self.queue:
                filename, name, author = self.queue[0]  # Peek at first item
                self.queue.pop(0)  # Remove it after we know we have it
                
                ffmpeg_options = {
                    'options': '-vn -b:a 128k -bufsize 64k -ar 48000 -filter:a "loudnorm, volume=2.0"',
                }
                audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)
                voice_client.play(audio_source, after=lambda _: asyncio.run_coroutine_threadsafe(self.play_next(ctx, voice_client), self.bot.loop))
                
                await send(self.bot, ctx, title="Now Playing", content=f"🎵 Playing {name} by {author}", color=0x2ECC71)
            elif not self.loop:
                await voice_client.disconnect()

    @commands.command(description="Stop the music")
    async def stop(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            voice_client.stop()
            await voice_client.disconnect()
            await send(self.bot, ctx, title="Stopped", content="🎵 Stopped the music.", color=0xE74C3C)
        else:
            await send(self.bot, ctx, title="Error", content="I'm not connected to a voice channel.", color=0xFF0000)

    @commands.command(description="Add a song to the queue")
    async def add(self, ctx, query):
        info, error = await self.search_yt(query)
        if error:
            await send(self.bot, ctx, title="Error", content=f"Error: {error}", color=0xFF0000)
            return

        name = info['title']
        author = info['uploader']
        self.queue.append((query, name, author))
        await send(self.bot, ctx, title="Added to Queue", content=f"🎵 Added {name} by {author} to the queue.", color=0x2ECC71)

    @commands.command(description="View the queue")
    async def queue(self, ctx):
        if not self.queue:
            await send(self.bot, ctx, title="Queue", content="🎵 The queue is empty.", color=0xFF0000)
            return

        queue_text = "\n".join(f"{i+1}. {name} by {author}" for i, (_, name, author) in enumerate(self.queue))
        await send(self.bot, ctx, title="Current Queue", content=f"🎵 {queue_text}", color=0x2ECC71)

    @commands.command(description="Toggle loop")
    async def loop(self, ctx):
        self.loop = not self.loop
        status = "enabled" if self.loop else "disabled"
        await send(self.bot, ctx, title="Loop", content=f"🎵 Looping is now {status}.", color=0x2ECC71 if self.loop else 0xE74C3C)

    @commands.command(description="Skip the current song")
    async def skip(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            await send(self.bot, ctx, title="Error", content="Not playing anything right now!", color=0xFF0000)
            return
        
        if not voice_client.is_playing():
            await send(self.bot, ctx, title="Error", content="No song is currently playing!", color=0xFF0000)
            return

        voice_client.stop()  # This will trigger the after callback in play() which calls play_next
        await send(self.bot, ctx, title="Skipped", content="🎵 Skipped the current song.", color=0x2ECC71)

async def setup(bot):
    await bot.add_cog(Music(bot))
