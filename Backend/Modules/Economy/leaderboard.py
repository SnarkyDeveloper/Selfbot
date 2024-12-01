import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="View the leaderboard")
    async def leaderboard(self, ctx):
        data = self.db.get_leaderboard()
        await ctx.send(data)
        
async def setup(bot):
    
    await bot.add_cog(Leaderboard(bot))