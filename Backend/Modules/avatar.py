import discord
from discord.ext import commands
import asyncio
import os
from Backend.utils import check_permissions

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="avatar", description="Get the avatar of a user", aliases=["av"])
    async def avatar(self, ctx, user=None):
        if not check_permissions(ctx.author):
            return
        
        if user is None:
            member = ctx.author
        else:
            try:
                # Try to convert the input to a member object
                member = await commands.MemberConverter().convert(ctx, user)
            except commands.MemberNotFound:
                await ctx.send("User not found!")
                return
        
        avatar_url = member.display_avatar.url
        await ctx.send(avatar_url)
    @commands.command(name="avatar_server", description="Get the avatar of the server", aliases=["as"])
    async def avatar_server(self, ctx):
        if not check_permissions(ctx.author):
            return
        
        # Get the user's server-specific avatar
        guild_avatar = ctx.author.guild_avatar
        if guild_avatar:
            await ctx.send(guild_avatar.url)
        else:
            await ctx.send("You don't have a server-specific avatar!")
    @commands.command(name="banner", description="Get the banner of a user")
    async def banner(self, ctx, user: discord.Member = None):
        if not check_permissions(ctx.author):
            return
        if user is None:
            user = ctx.author
        if user.banner:
            await ctx.send(f"{user.banner.url}")
        else:
            await ctx.send("The user doesn't have a banner!")
            
async def setup(bot):
    await bot.add_cog(Avatar(bot))