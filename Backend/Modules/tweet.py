import json
import httpx
from Backend.send import send
from discord.ext import commands

class Tweet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(description="Create a fake tweet")
    async def tweet(self, ctx, *, tweet: str):
        if not tweet:
            await send(self.bot, ctx, title='Error', content='Please provide a tweet in the format: <username>:<tweet>', color=0xff0000)
            return
        tweet = tweet.split(':')
        if len(tweet) != 2:
            name = ctx.author.name
            content= tweet[0]
        else: 
            name = tweet[0]
            content = tweet[1]
        response = httpx.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={name}&displayname={name}&text={content}")
        response = json.loads(response.text)
        await send(self.bot, ctx, title='Tweet', image=response['message'])
async def setup(bot):
    await bot.add_cog(Tweet(bot))