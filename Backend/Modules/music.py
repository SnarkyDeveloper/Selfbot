import discord, asyncio, os, yt_dlp, glob, sys
from discord.ext import commands
from pytube import Search
from Backend.utils import check_permissions
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def download_song(self, query):
        stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        try:
            search_query = f"{query} (lyrics)"
            s = Search(search_query)
            if not s.results:
                s = Search(query)
                if not s.results:
                    return None, "No results found."
            
            for result in s.results:
                channel_name = result.author
                if any(label in channel_name.lower() for label in [
                    'vevo', 'official', 'records', 'music'
                ]):
                    video_id = result.video_id
                    break
            else:
                video_id = s.results[0].video_id
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            audio_dir = os.path.normpath(os.path.join(current_dir, '../../audio'))
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(audio_dir, '%(title)s.%(ext)s'),
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
        
    @commands.command(description='Play a song')
    async def play(self, ctx, query):
        if not check_permissions(ctx.author):
            return
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
    @commands.command(description='Stop the music')
    async def stop(self, ctx):
        if not check_permissions(ctx.author):
            return
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect(force=True)
        else:
            await ctx.send("No music is currently playing.")

    @commands.command(description='Pause the music')
    async def pause(self, ctx):
        if not check_permissions(ctx.author):
            return
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("🎵 Paused the music.")
    @commands.command(description='Resume the music')
    async def resume(self, ctx):
        if not check_permissions(ctx.author):
            return
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("🎵 Resumed the music.")

            
async def setup(bot):
    await bot.add_cog(Music(bot))