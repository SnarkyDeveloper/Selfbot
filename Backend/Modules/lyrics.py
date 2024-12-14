import discord
from discord.ext import commands
import httpx
from urllib.parse import quote_plus
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
        query = query.lower()
        title, artist = None, None
        if "/" in query:
            title, artist = query.split("/", 1)
        elif "-" in query:
            title, artist = query.split("-", 1)
        elif " by " in query:
            title, artist = query.split(" by ", 1)

        if artist and title:
            url = f"https://api.lyrics.ovh/v1/{quote_plus(artist.strip())}/{quote_plus(title.strip())}"
            response = httpx.get(url)
            lyrics = ". ".join([line for line in response.json()["lyrics"].splitlines() if line.strip()])
            if response.json().get('error'):
                await ctx.send("Lyrics not found.")
            else:
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
        else:
            await ctx.send("Please provide the song in 'title by artist' format.")
async def setup(bot):
    await bot.add_cog(Lyrics(bot))