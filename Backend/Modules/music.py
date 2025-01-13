import discord
import asyncio
import os
import yt_dlp
import glob
from discord.ext import commands
from ytmusicapi import YTMusic
from Backend.send import send
from typing import Optional, Tuple

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ytmusic = YTMusic()
        self.queues = {}
        self.loops = {}
        self.current_tracks = {}
        self.now_playing_messages = {}
        self.audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'audio')
        os.makedirs(self.audio_dir, exist_ok=True)
        self.volume = 100

    async def search_yt(self, query: str) -> Tuple[Optional[dict], Optional[str]]:
        try:
            search_results = self.ytmusic.search(query, filter="songs")
            if not search_results:
                return None, "No results found."
            
            video_id = search_results[0]['videoId']
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info, None
            
        except Exception as e:
            return None, f"Search error: {str(e)}"

    async def download_song(self, query: str, ctx) -> Tuple[Optional[dict], Optional[str], Optional[str]]:
        try:
            info, error = await self.search_yt(query)
            if error:
                return None, error, None

            safe_title = f"{info['title']}-{info['uploader']}".replace(' ', '_').encode("ascii", errors="ignore").decode()
            file_path = os.path.join(self.audio_dir, f"{safe_title}.mp3")
        
            if not os.path.exists(file_path):
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': file_path[:-4],
                    'no_warnings': True,
                    'extract_audio': True,
                    'audio_format': 'mp3',
                    'prefer_ffmpeg': True
                }
            
                async with ctx.typing():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([info['webpage_url']])
                
            await self._clean_old_files()
            return info, None, file_path
            
        except Exception as e:
            return None, f"Download error: {str(e)}", None

    def _get_queue_id(self, ctx) -> str:
        return str(ctx.guild.id if ctx.guild else ctx.author.id)

    def _get_queue(self, ctx) -> list:
        queue_id = self._get_queue_id(ctx)
        if queue_id not in self.queues:
            self.queues[queue_id] = []
        return self.queues[queue_id]

    async def _clean_old_files(self, max_files=50):
        try:
            audio_files = glob.glob(os.path.join(self.audio_dir, '*.mp3'))
            while len(audio_files) > max_files:
                oldest_file = min(audio_files, key=os.path.getctime)
                try:
                    os.remove(oldest_file)
                    audio_files = glob.glob(os.path.join(self.audio_dir, '*.mp3'))
                except OSError:
                    break
        except Exception:
            pass

    async def connect_to_voice(self, ctx) -> Optional[discord.VoiceClient]:
        if not ctx.author.voice:
            await send(self.bot, ctx, title="Error", content="Join a voice channel first!", color=0xFF0000)
            return None

        target_channel = ctx.author.voice.channel
        target_guild = ctx.guild if ctx.guild else target_channel.guild

        for vc in self.bot.voice_clients:
            if vc.guild == target_guild:
                await vc.disconnect(force=True)

        try:
            return await target_channel.connect()
        except Exception as e:
            await send(self.bot, ctx, title="Error", content=f"Failed to connect: {str(e)}", color=0xFF0000)
            return None

    @commands.command(description="Play music")
    async def play(self, ctx, query: str):
        queue = self._get_queue(ctx)
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild if ctx.guild else None)

        if not voice_client:
            voice_client = await self.connect_to_voice(ctx)
            if not voice_client:
                return

        await ctx.message.add_reaction('🔎')
        info, error, file_path = await self.download_song(query, ctx)
            
        if error:
            await send(self.bot, ctx, title="Error", content=error, color=0xFF0000)
            await ctx.message.remove_reaction('🔎', self.bot.user)
            if not queue:
                await voice_client.disconnect()
            return

        artist = info.get('uploader', 'Unknown')
        if artist.endswith("- Topic"):
            artist = artist[:-8].strip()
        queue_entry = (file_path, info['title'], artist)
        queue.append(queue_entry)
        await ctx.message.remove_reaction('🔎', self.bot.user)
        if not voice_client.is_playing():
            await self._play_next(ctx, voice_client)
        else:
            await send(self.bot, ctx, title="Added to Queue", 
                      content=f"🎵 Added {info['title']} by {artist}", color=0x2ECC71)

    async def _play_next(self, ctx, voice_client: discord.VoiceClient):
        if not voice_client or not voice_client.is_connected():
            return

        queue = self._get_queue(ctx)
        queue_id = self._get_queue_id(ctx)
        if queue_id in self.now_playing_messages:
            try:
                await self.now_playing_messages[queue_id].delete()
            except:
                pass
        if self.loops.get(queue_id, False) and self.current_tracks.get(queue_id):
            title, author = self.current_tracks[queue_id]
            file_path = os.path.join(self.audio_dir, f"{title.replace(' ', '_')}.mp3")
            queue.append((file_path, title, author))

        if not queue:
            if not self.loops.get(queue_id, False):
                await voice_client.disconnect()
                self.current_tracks[queue_id] = None
            return

        file_path, title, author = queue[0]
        if self.loops.get(queue_id, False):
            queue.append(queue.pop(0))
        else:
            queue.pop(0)

        self.current_tracks[queue_id] = (title, author)

        try:
            audio_source = discord.FFmpegPCMAudio(
                file_path,
                options=f'-vn -b:a 128k -bufsize 64k -ar 48000 -filter:a "volume={self.volume/100}"'
            )
        
            voice_client.play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self._handle_playback_error(e, ctx, voice_client),
                    self.bot.loop
                )
            )
            message = await send(self.bot, ctx, title="Now Playing", content=f"🎵 Playing {title} by {author}", color=0x2ECC71)
            self.now_playing_messages[queue_id] = message
        
        except Exception as e:
            await send(self.bot, ctx, title="Error", 
                      content=f"Playback error: {str(e)}", color=0xFF0000)
            await self._play_next(ctx, voice_client)

    async def _handle_playback_error(self, error, ctx, voice_client):
        if error:
            await send(self.bot, ctx, title="Error", 
                      content=f"Playback error: {str(error)}", color=0xFF0000)
        await self._play_next(ctx, voice_client)

    @commands.command(description="Set volume (0-200)")
    async def volume(self, ctx, volume: int):
        volume = int(volume)
        if not 0 <= volume <= 200:
            await send(self.bot, ctx, title="Error", 
                      content="Volume must be between 0 and 200", color=0xFF0000)
            return
            
        self.volume = volume
        await send(self.bot, ctx, title="Volume", 
                  content=f"Volume set to {volume}%", color=0x2ECC71)

    @commands.command(description="Show current queue")
    async def queue(self, ctx):
        queue = self._get_queue(ctx)
        
        if not queue:
            await send(self.bot, ctx, title="Queue Empty", 
                      content="📝 No tracks in queue", color=0xFF0000)
            return

        queue_text = "\n".join(f"{i+1}. {title} by {author}" 
                             for i, (_, title, author) in enumerate(queue))
        await send(self.bot, ctx, title="Current Queue", 
                  content=f"📝 {queue_text}", color=0x2ECC71)

    @commands.command(description="Toggle loop mode")
    async def loop(self, ctx):
        queue_id = self._get_queue_id(ctx)
        self.loops[queue_id] = not self.loops.get(queue_id, False)
        status = "enabled" if self.loops[queue_id] else "disabled"
        await send(self.bot, ctx, title="Loop", 
                  content=f"🔄 Loop mode {status}", color=0x2ECC71)
    @commands.command(name="now", description="Show current track")
    async def now_playing(self, ctx):
        queue_id = self._get_queue_id(ctx)
        current = self.current_tracks.get(queue_id)
        
        if not current:
            await send(self.bot, ctx, title="Not Playing", 
                      content="Nothing is playing right now", color=0xFF0000)
            return
            
        title, author = current
        await send(self.bot, ctx, title="Now Playing", 
                  content=f"🎵 {title} by {author}", color=0x2ECC71)
    @commands.command(description="Skip current track")
    async def skip(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild if ctx.guild else None)
        
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction('⏭️')
        else:
            await send(self.bot, ctx, title="Cannot Skip", content="Nothing is playing!", color=0xFF0000)

    @commands.command(description="Stop playback and clear queue")
    async def stop(self, ctx):
        queue_id = self._get_queue_id(ctx)
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild if ctx.guild else None)
        
        if voice_client and voice_client.is_connected():
            self.queues[queue_id] = []
            self.current_tracks[queue_id] = None
            voice_client.stop()
            await voice_client.disconnect()
            await send(self.bot, ctx, title="Stopped", content="⏹️ Playback stopped and queue cleared", color=0x2ECC71)
        else:
            await send(self.bot, ctx, title="Cannot Stop", content="Not connected to a voice channel!", color=0xFF0000)

async def setup(bot):
    await bot.add_cog(Music(bot))