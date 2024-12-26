import discord
from discord.ext import commands
import asyncio

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", description="Get the avatar of a user", aliases=["av"])
    async def avatar(self, ctx, user: discord.Member = None):

        member = user or ctx.author
        avatar_url = member.display_avatar.url
        await ctx.send(avatar_url)

    @commands.command(name="avatar_server", description="Get the avatar of the server", aliases=["as"])
    async def avatar_server(self, ctx):

        guild_avatar = ctx.author.guild_avatar
        if guild_avatar:
            await ctx.send(guild_avatar.url)
        else:
            await ctx.send("You don't have a server-specific avatar!")

    @commands.command(name="banner", description="Get the banner of a user")
    async def banner(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author.id
        else:
            user = int(str(user).strip('<@!>'))
        user_data = await self.bot.fetch_user(user)
        if user_data.banner:
            await ctx.send(user_data.banner.url)
        else:
            await ctx.send("The user doesn't have a banner!")

async def setup(bot):
    await bot.add_cog(Avatar(bot))
