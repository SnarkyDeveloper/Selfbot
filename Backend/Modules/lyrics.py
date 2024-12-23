import discord
from discord.ext import commands
import json
from urllib.parse import quote_plus
import lyrical

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
        lyrics_data = json.loads(await lyrical.Lyrics.lyrics(query))
        title = lyrics_data['title']
        artist = lyrics_data['artists']
        lyrics = lyrics_data['lyrics']
        try:
            await ctx.send(f'# Lyrics of {title.strip()} by {artist.strip()}:\n ```{lyrics}```')
        except discord.HTTPException:
            lyrics_parts = split_string_into_list(lyrics, 1993)
            for index, part in enumerate(lyrics_parts):
                if index == 0:
                    await ctx.send(f'# Lyrics of {title.strip()} by {artist.strip()}')
                await ctx.send(f'```{part}```')

async def setup(bot):
    await bot.add_cog(Lyrics(bot))
