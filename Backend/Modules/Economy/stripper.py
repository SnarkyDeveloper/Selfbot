import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
import random
from datetime import datetime, timedelta

performance = [1, 2, 3]

class Stripper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Work as a stripper")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def stripper_cmd(self, ctx):
        print("Stripper command called")
        try:
            data = self.db.get_cooldown(ctx.author.id, "last_stripper")
            if data:
                time_diff = datetime.now().timestamp() - data
                if time_diff < 300:
                    remaining = 300 - time_diff
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    await ctx.send(f"You need to wait {minutes} minutes and {seconds} seconds before stripping again!")
                    return

            performance_multiplier = random.choice(performance)
            if performance_multiplier == 1:
                self.db.remove_balance(ctx.author.id, 100)
                await ctx.send(f"{ctx.author.mention} worked as a stripper, but didn't perform well and lost $100!")
            elif performance_multiplier == 2:
                money = random.randint(100, 300)
                self.db.add_balance(ctx.author.id, money)
                await ctx.send(f"{ctx.author.mention} worked as a stripper, and performed alright, earning **${money}**!")
            else:
                money = random.randint(300, 500)
                self.db.add_balance(ctx.author.id, money)
                await ctx.send(f"{ctx.author.mention} has worked as a stripper and did excellently, earning **${money}**!")

            data = self.db.read_eco()
            for entry in data["users"]:
                if entry["user"] == str(ctx.author.id):
                    entry["last_stripper"] = datetime.now().timestamp()
                    self.db.write_eco(data)
                    return

        except Exception as e:
            print(f"Error in stripper command: {e}")
            await ctx.send("An error occurred while processing the stripper command.")

async def setup(bot):
    stripper_cog = Stripper(bot)
    stripper_cmd = stripper_cog.stripper_cmd
    bot.eco.add_command(stripper_cmd)
    await bot.add_cog(stripper_cog)