import discord
from discord.ext import commands
import json
from urllib.parse import quote_plus
import lyrical
from Backend.send import send
def split_string_into_list(input_string, max_length):
    lyrics = []
    while len(input_string) > max_length:
        split_index = input_string.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        lyrics.append(input_string[:split_index].strip())
        input_string = input_string[split_index:].lstrip('\n')
    lyrics.append(input_string.strip())
    return lyrics

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(description="Get lyrics for a song")
    async def lyrics(self, ctx, query: str):
        if not query:
            await ctx.send("Please provide a song name.")
            return
        lyrics_data = await lyrical.Lyrics.lyrics(query)
        if not lyrics_data:
            await send(self.bot, ctx, title='Error', content="No lyrics found.", color=0xff0000)
            return
        else:
            lyrics_data = json.loads(lyrics_data)
        title = lyrics_data['title']
        artist = lyrics_data['artists']
        lyrics = lyrics_data['lyrics']
        try:
            await send(self.bot, ctx, title=f'Lyrics of {title.strip()} by {artist.strip()}', content=lyrics)
        except:
            send(self.bot, ctx, content='Issue retrieving lyrics', title='Error', color=0xff0000)

async def setup(bot):
    await bot.add_cog(Lyrics(bot))
