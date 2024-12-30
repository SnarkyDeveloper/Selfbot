from discord.ext import commands
import httpx
from Backend.send import send
class qotd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(Description="Get the quote of today")
    async def qotd(self, ctx):
        quote = httpx.get("https://zenquotes.io/api/today")
        await send(self.bot, ctx, title="Quote of the Day", content=f'{quote.json()[0]["q"]}\n\u2014 {quote.json()[0]["a"]}', color=0xFEE75C)
    @commands.command(Description="Get a random quote", aliases=["rq"])
    async def randomquote(self, ctx):
        quote = httpx.get("https://zenquotes.io/api/random")
        await send(self.bot, ctx, title="Random Quote", content=f'{quote.json()[0]["q"]}\n\u2014 {quote.json()[0]["a"]}', color=0xFEE75C)
async def setup(bot):
    await bot.add_cog(qotd(bot))