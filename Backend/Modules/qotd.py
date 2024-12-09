import json
import discord
from discord.ext import commands
import httpx
class qotd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(Description="Get the quote of today")
    async def qotd(self, ctx):
        quote = httpx.get("https://zenquotes.io/api/today")
        await ctx.send(quote.json()[0]["q"] + "\n\u2014 " + quote.json()[0]["a"])
    @commands.command(Description="Get a random quote", aliases=["rq"])
    async def randomquote(self, ctx):
        quote = httpx.get("https://zenquotes.io/api/random")
        await ctx.send(quote.json()[0]["q"] + "\n\u2014 " + quote.json()[0]["a"])
async def setup(bot):
    await bot.add_cog(qotd(bot))