import discord
from discord.ext import commands
import asyncio
import os
from Backend.utils import check_permissions

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Test(bot))