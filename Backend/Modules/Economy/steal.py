import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
import random
from datetime import datetime
# mafia_phrases = ["has helped with a drug deal", "has helped with a robbery", "has helped with a kidnapping", "has helped with a hit", "has helped with a murder", "has helped with a extortion", "has helped with a blackmail", "has helped with a prostitution ring", "has helped with a human trafficking ring", "has helped with a arms dealing", "has helped with a arms smuggling", "has helped with a arms trafficking", "has helped with a arms manufacturing", "has helped with a arms dealing", "has helped with a arms smuggling", "has helped with a arms trafficking", "has helped with a arms manufacturing"]
class Steal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Steal money from another user")
    @commands.cooldown(1, 420, commands.BucketType.user)  # 7 minutes
    async def steal_cmd(self, ctx, target: discord.Member):
        print(f"Steal command called with target: {target}")
        try:
            if target == ctx.author:
                await ctx.send("You can't steal from yourself!")
                return
            
            target_balance = self.db.get_balance(target.id)
            if target_balance < 100:
                await ctx.send(f"{ctx.author.mention}, that user is too poor to steal from!")
                return

            steal_amount = min(random.randint(50, 200), target_balance)
            self.db.steal(ctx.author.id, target.id, steal_amount)
            await ctx.send(f"{ctx.author.mention} has stolen **${steal_amount}** from {target.mention}!")

        except Exception as e:
            print(f"Error in steal command: {e}")
            await ctx.send("An error occurred while processing the steal command.")

    # @commands.command(description="Work with the mafia")
    # @commands.cooldown(1, 420, commands.BucketType.user)
    # async def mafia(self, ctx): 
    #     try:
    #         caught = random.choice([True, False])
    #         if caught:
    #             self.db.remove_balance(ctx.author.id, 1000)
    #             await ctx.send(f"{ctx.author.mention} was caught by the police and was fined $1000!")
    #         else:
    #             money = random.randint(1000, 5000)
    #             self.db.add_balance(ctx.author.id, money)
    #             await ctx.send(f"{ctx.author.mention} {random.choice(mafia_phrases)} and earned **${money}**!")
    #     except Exception as e:
    #         print(f"Error in mafia command: {e}")
    #         await ctx.send("An error occurred while processing the mafia command.")

async def setup(bot):
    steal_cog = Steal(bot)
    steal_cmd = steal_cog.steal_cmd
    steal_cmd.name = "steal"
    bot.eco.add_command(steal_cmd)
    await bot.add_cog(steal_cog)