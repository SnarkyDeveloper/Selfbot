import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
import random
from Backend.send import send
class Steal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Steal money from another user")
    @commands.cooldown(1, 420, commands.BucketType.user)
    async def steal_cmd(self, ctx, target: discord.Member):
        print(f"Steal command called with target: {target}")
        try:
            if target == ctx.author:
                await send(self.bot, ctx, title="Error", content="You can't steal from yourself!", color=0xFF0000)
                return
            
            target_balance = self.db.get_balance(target.id)
            if target_balance < 100:
                await send(self.bot, ctx, title="Haha Pooron!", content=f"{ctx.author.mention}, that user is too poor to steal from!", color=0xE74C3C)
                return

            steal_amount = min(random.randint(50, 200), target_balance)
            self.db.steal(ctx.author.id, target.id, steal_amount)
            await send(self.bot, ctx, title="Success!", content=f"{ctx.author.mention} has stolen **${steal_amount}** from {target.mention}!", color=0x2ECC71)

        except Exception as e:
            print(f"Error in steal command: {e}")
            await send(self.bot, ctx, title="Error", content="An error occurred while processing the steal command.", color=0xFF0000)


async def setup(bot):
    steal_cog = Steal(bot)
    steal_cmd = steal_cog.steal_cmd
    steal_cmd.name = "steal"
    bot.eco.add_command(steal_cmd)
    await bot.add_cog(steal_cog)