import discord
from discord.ext import commands
import httpx
from urllib.parse import quote_plus
import lyrical
def split_string_into_list(input_string, max_length):
    lyrics = []
    while len(input_string) > max_length:
        lyrics.append(input_string[:max_length])
        input_string = input_string[max_length:]
    lyrics.append(input_string)
    return lyrics
class Lyrics(commands.Cog):
    def __init__(self, bot):
        print("Lyrics cog loaded")
        self.bot = bot 

    @commands.command(description="Get lyrics for a song")
    async def lyrics(self, ctx, query: str):
        if not query:
            await ctx.send("Please provide a song name.")
            return
        lyrics =lyrical.Lyrics.lyrics(query)
        title = lyrics['title']
        artist = lyrics['artist']
        lyrics = lyrics['lyrics']
        try:
            await ctx.send(f'# Lyrics of {title.strip()} by {artist.strip()}:\n ```{lyrics}```')
        except discord.HTTPException:
            lyrics = split_string_into_list(lyrics, 1993)
            for index, lyric in enumerate(lyrics):
                if index == 0:
                    await ctx.send(f'# Lyrics of {title.strip()} by {artist.strip()}')
                    await ctx.send(f'```{lyric}```')
                else:
                    await ctx.send(f'```{lyric}```')
async def setup(bot):
    await bot.add_cog(Lyrics(bot))