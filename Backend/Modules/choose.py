import random
from discord.ext import commands
from Backend.utils import check_permissions, CommandHelper

class Choose(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, choices: str):
        if check_permissions(ctx.author):
            helper = CommandHelper(ctx)
            choice_list = choices.split()
            await helper.send(random.choice(choice_list))
        else:
            pass

async def setup(bot):
    await bot.add_cog(Choose(bot))