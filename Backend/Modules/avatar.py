import discord
from discord.ext import commands
import asyncio
from Backend.send import send
class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(description="Get the avatar of a user", aliases=['av'])
    async def avatar(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        await send(self.bot, ctx, title=f'{user.global_name}\'s Avatar', image=user.avatar.url)

    @commands.command(name="avatar_server", description="Get the avatar of the server", aliases=["as"])
    async def avatar_server(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        guild_avatar = user.guild_avatar
        if guild_avatar:
            await send(self.bot, ctx, title="Server Avatar", image=user.guild_avatar.url)
        else:
            await send(self.bot, ctx, title=f'Error', content="The server doesn't have a server specific avatar!", color=0xFF0000)
    @commands.command(name="banner", description="Get the banner of a user")
    async def banner(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author.id
        user_data = await self.bot.fetch_user(user)
        if user_data.banner:
            await send(self.bot, ctx, title=f'{user_data.global_name}\'s Banner', image=user_data.banner.url)
        else:
            await send(self.bot, ctx, title=f'Error', content="The user doesn't have a banner!", color=0xFF0000)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
