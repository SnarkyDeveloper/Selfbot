import discord, asyncio, os, yt_dlp, glob, sys
from discord.ext import commands
from ytmusicapi import YTMusic
from Backend.send import send
queue = []
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ytmusic = YTMusic()
        self.loop = False
        self.skip = False
    async def search_yt(self, query):
        search_query = f"{query}"
        s = self.ytmusic.search(search_query)
        if not s[0]:
            return None, "No results found."
        video_id = s[0]['videoId']
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)

        return info, None
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
                'outtmpl': os.path.join(audio_dir, '%(title)s.%(ext)s'),
            }
            
            os.makedirs(audio_dir, exist_ok=True)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"
                
                if not os.path.exists(filename):
                    print(f"Downloading new song: {info['title']} by {info['uploader']}")
                    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
                else:
                    print(f"Song already exists: {info['title']} by {info['uploader']}")
            
            audio_files = glob.glob(os.path.join(audio_dir, '*.mp3'))
            while len(audio_files) >= 30: #change as needed, storage is tight sometimes i know
                oldest_file = min(audio_files, key=os.path.getctime)
                os.remove(oldest_file)
                audio_files = glob.glob(os.path.join(audio_dir, '*.mp3'))
            
            return info, None, filename
            
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
                
                await send(self.bot, ctx, title='🔍 Searching', content=f"Searching for: {query}", color=0xFEE75C)
                download_task = asyncio.create_task(self.download_song(query))
                
                print(f"Connecting to channel: {voice_channel}")
                voice_client = await voice_channel.connect()
                print("Connected to voice channel")
                await send(self.bot, ctx, title='Joined', content="🎵 Joined voice channel, Playing...")
                
                info, error, filename = await download_task
                if error:
                    await voice_client.disconnect()
                    await send(self.bot, ctx, title='Error', content=f"Error: {error}", color=0xff0000)
                    return
                name = info['title']
                author = info['uploader']
                ffmpeg_options = {
                    'options': '-vn -b:a 128k -bufsize 64k -ar 48000 -filter:a "loudnorm, volume=2.0"',
                }

                
                print("Creating audio source...")
                audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)
                print("Audio source created")
                
                print("Starting playback...")
                voice_client.play(audio_source)
                await send(self.bot, ctx, title='Now playing', content=f'🎵 Playing {name} by {author}...', color=0x2ECC71)
                
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

                    # Song end logic
                    if self.skip == True:
                        self.skip = False
                        if len(queue) > 0:
                            filename, name, author = queue.pop(0)
                            await send(self.bot, ctx, title='Now playing', content=f'🎵 Playing {name} by {author}...', color=0x2ECC71)
                            audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)  
                            voice_client.play(audio_source)
                            if self.loop:
                                queue.append((filename, name, author))
                    if not voice_client.is_playing() and not voice_client.is_paused():
                        if len(queue) > 0:
                            print("Downloading next song...")
                            download_task = asyncio.create_task(self.download_song(queue[0][1]))
                            info, error, filename = await download_task
                            if error:
                                await send(self.bot, ctx, title='Error', content=f"Error playing song: {error}", color=0xff0000)
                                return
                            filename, name, author = queue.pop(0)
                            await send(self.bot, ctx, title='Now playing', content=f'🎵 Playing {name} by {author}...', color=0x2ECC71)
                            audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)  
                            voice_client.play(audio_source)     
                            if self.loop:
                                queue.append((filename, name, author))
                        elif self.loop:
                            print("Looping song...")
                            audio_source = discord.FFmpegPCMAudio(filename, **ffmpeg_options)  
                            voice_client.play(audio_source)
                            await send(self.bot, ctx, title='Now playing', content=f'🎵 Playing {name} by {author}...', color=0x2ECC71)
                        else:
                            print("Playback finished")
                            await voice_client.disconnect()
                            self.loop = False
                            break

                    await asyncio.sleep(1)
                                    
            except Exception as e:
                print(f"Error: {str(e)}")
                await send(self.bot, ctx, title='Error', content=f"Error: {str(e)}", color=0xff0000)
                if 'voice_client' in locals() and voice_client.is_connected():
                    await voice_client.disconnect()
        else:
            await send(self.bot, ctx, title='Error', content='You need to be in a voice channel to use this command!', color=0xff0000)
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
            await send(self.bot, ctx, title='Stopped', content="🎵 Stopped the music.", color=0xE74C3C)
        else:
            await send(self.bot, ctx, title='Error', content="You need to be in a voice channel to use this command.", color=0xff0000)

    @commands.command(description='Pause the music')
    async def pause(self, ctx):
        voice_client = await self.check_if_vc(ctx)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await send(self.bot, ctx, title='Paused', content="🎵 Paused the music.", color=0xFEE75C)
        else:
            await send(self.bot, ctx, title='Error', content="Nothing is playing right now.", color=0xff0000)

    @commands.command(description='Resume the music')
    async def resume(self, ctx):
        voice_client = await self.check_if_vc(ctx)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await send(self.bot, ctx, title='Resumed', content="🎵 Resumed the music.", color=0x2ECC71)
        else:
            await send(self.bot, ctx, title='Error', content="Nothing is paused right now.", color=0xff0000)
    @commands.command(description='Add a song to the queue')
    async def add(self, ctx, query):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                info, error = await self.search_yt(query)
                if error:
                    await send(self.bot, ctx, title='Error', content=f"Error: {error}", color=0xff0000)
                    return
                name = info['title']
                author = info['uploader']
                queue.append((query, name, author))
                await send(self.bot, ctx, title='Added to queue', content=f'🎵 Added {name} by {author} to queue.', color=0x2ECC71)
        else:
            await send(self.bot, ctx, title='Error', content="🎵 I'm not connected to a voice channel.", color=0xff0000)

    @commands.command(description='View the queue')
    async def queue(self, ctx):
        if not queue:
            await send(self.bot, ctx, title='Error', content="🎵 Queue is empty!", color=0xff0000)
            return
        
        queue_text = ''
        for i, (name, author) in enumerate(queue, 1):
            queue_text += f"{i}. {name} by {author}\n"
        
        await send(self.bot, ctx, title='Current Queue 🎵', content=queue_text, color=0x2ECC71)
    @commands.command(description='Loop the queue')
    async def loop(self, ctx):
        if self.loop:
            self.loop = False
            await send(self.bot, ctx, title='Loop off', content="🎵 Loop off.", color=0xE74C3C)
        else:
            self.loop = True
            await send(self.bot, ctx, title='Looping', content="🎵 Looping on.", color=0x2ECC71)
    @commands.command(description='Skip the current song')
    async def skip(self, ctx):
        voice_client = await self.check_if_vc(ctx)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await send(self.bot, ctx, title='Skipped', content="🎵 Skipped the current song.", color=0xE74C3C)
            self.skip = True
        else:
                await send(self.bot, ctx, title='Error', content="Nothing is playing right now.", color=0xff0000)
async def setup(bot):
    await bot.add_cog(Music(bot))