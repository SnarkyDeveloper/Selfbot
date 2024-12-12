import discord, asyncio, os, yt_dlp, glob, sys
from discord.ext import commands
from ytmusicapi import YTMusic
from Backend.utils import check_permissions
queue = []
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ytmusic = YTMusic()
    async def download_song(self, query):
        stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        try:
            search_query = f"{query}"
            s = self.ytmusic.search(search_query)
            if not s[0]:
                return None, "No results found."
            video_id = s[0]['videoId']
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            audio_dir = os.path.normpath(os.path.join(current_dir, '../../audio'))
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(audio_dir, '%(title)s.%(ext)s'),  # Changed to ensure .mp3 extension
            }
            
            os.makedirs(audio_dir, exist_ok=True)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"
                
                if not os.path.exists(filename):
                    print(f"Downloading new song: {info['title']}")
                    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
                else:
                    print(f"Song already exists: {info['title']}")
            
            audio_files = glob.glob(os.path.join(audio_dir, '*.mp3'))
            while len(audio_files) >= 30:
                oldest_file = min(audio_files, key=os.path.getctime)
                os.remove(oldest_file)
                audio_files = glob.glob(os.path.join(audio_dir, '*.mp3'))
            
            return filename, None
            
        except Exception as e:
            return None, str(e)
        finally:
            sys.stderr = stderr
        
# -------------- PLAYBACK ------------
    @commands.command(description='Play a song')
    async def play(self, ctx, query):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            try:
                print("Starting play command...")
                for vc in ctx.bot.voice_clients:
                    if vc.guild == ctx.guild:
                        print("Force disconnecting from voice...")
                        await vc.disconnect(force=True)
                
                await ctx.send(f"🔍 Searching for: {query}")
                download_task = asyncio.create_task(self.download_song(query))
                
                print(f"Connecting to channel: {voice_channel}")
                voice_client = await voice_channel.connect()
                print("Connected to voice channel")
                await ctx.send("🎵 Joined voice channel, Playing...")
                
                filename, error = await download_task
                if error:
                    await voice_client.disconnect()
                    await ctx.send(f"Error: {error}")
                    return
                
                ffmpeg_options = {
                    'options': '-vn -b:a 128k -bufsize 64k -ar 48000',
                }
                
                print("Creating audio source...")
                audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)
                print("Audio source created")
                
                print("Starting playback...")
                voice_client.play(audio_source)
                await ctx.send('🎵 Now playing...')
                
                while voice_client.is_connected():
                    if isinstance(voice_channel, discord.VoiceChannel):
                        if ctx.author not in voice_channel.members:
                            print("Command author left voice channel")
                            if voice_client.is_playing():
                                voice_client.stop()
                            await voice_client.disconnect()
                            break
                    else:
                        if not ctx.author.voice or ctx.author.voice.channel != voice_channel:
                            print("Command author left voice channel")
                            if voice_client.is_playing():
                                voice_client.stop()
                            await voice_client.disconnect()
                            break
                            
                    if not voice_client.is_playing() and not voice_client.is_paused():
                        print("Playback finished")
                        await voice_client.disconnect()
                        break
                    await asyncio.sleep(1)
                    
            except Exception as e:
                print(f"Error: {str(e)}")
                await ctx.send(f"Error: {str(e)}")
                if 'voice_client' in locals() and voice_client.is_connected():
                    await voice_client.disconnect()
        else:
            await ctx.send('You need to be in a voice channel to use this command!')
    async def check_if_vc(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            return voice_client
        else:
            if ctx.author.voice and ctx.author.voice.channel:
                for vc in self.bot.voice_clients:
                    if vc.channel == ctx.author.voice.channel:
                        return vc
        return None

    @commands.command(description='Stop the music')
    async def stop(self, ctx):
        voice_client = await self.check_if_vc(ctx)
        if voice_client:
            voice_client.stop()
            await voice_client.disconnect(force=True)
            await ctx.send("🎵 Stopped the music.")
        else:
            await ctx.send("No music is currently playing.")

    @commands.command(description='Pause the music')
    async def pause(self, ctx):
        voice_client = await self.check_if_vc(ctx)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("🎵 Paused the music.")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command(description='Resume the music')
    async def resume(self, ctx):
        voice_client = await self.check_if_vc(ctx)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send("🎵 Resumed the music.")
        else:
            await ctx.send("Nothing is paused right now.")
    @commands.command(description='Add a song to the queue')
    async def addq(self, ctx, query):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                await ctx.send("🎵 Adding to the queue...")
                
        else:
            await ctx.send("🎵 I'm not connected to a voice channel.")
    @commands.command(description='View the queue')
    async def queue(self, ctx):
        pass
    @commands.command(description='Loop the queue')
    async def loop(self, ctx):
        pass
    
            
async def setup(bot):
    await bot.add_cog(Music(bot))