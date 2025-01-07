import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
from Backend.send import send

class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Shop for items")
    async def shop(self, ctx):
        await send(self.bot, ctx, title="Shop", content="Coming soon!", color=0xFF0000)

async def setup(bot):
    store_cog = Store(bot)
    store_cmd = store_cog.shop
    store_cmd.name = "shop"
    bot.eco.add_command(store_cmd)
    await bot.add_cog(store_cog)