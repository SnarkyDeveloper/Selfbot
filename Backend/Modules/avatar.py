import discord
from discord.ext import commands
from Backend.send import send
class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(description="Get the avatar of a user", aliases=['av'])
    async def avatar(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        else:
            user = await commands.UserConverter().convert(ctx, user)
        await send(self.bot, ctx, title=f'{user.global_name}\'s Avatar', image=user.avatar.url)

    @commands.command(name="sv", description="Get the avatar of the server", aliases=["as"])
    async def sv(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        else:
            user = await commands.UserConverter().convert(ctx, user)
        if user.guild_avatar:
            guild_avatar = user.guild_avatar
        if guild_avatar:
            await send(self.bot, ctx, title="Server Avatar", image=user.guild_avatar.url)
        else:
            await send(self.bot, ctx, title=f'Error', content="The server doesn't have a server specific avatar!", color=0xFF0000)
    @commands.command(name="banner", description="Get the banner of a user")
    async def banner(self, ctx, user: discord.Member = None):
        if not user:
            user = str(ctx.author.id)
        user = await commands.UserConverter().convert(ctx, user)
        if user.banner:
            await send(self.bot, ctx, title=f'{user.global_name}\'s Banner', image=user.banner.url)
        else:
            await send(self.bot, ctx, title=f'Error', content="The user doesn't have a banner!", color=0xFF0000)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
