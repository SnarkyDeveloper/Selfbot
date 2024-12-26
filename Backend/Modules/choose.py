import random
from discord.ext import commands

class Choose(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, choices: str):
        choice_list = choices.split()
        await ctx.send(random.choice(choice_list))
async def setup(bot):
    await bot.add_cog(Choose(bot))