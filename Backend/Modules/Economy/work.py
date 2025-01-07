import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
import random 
from datetime import datetime
from Backend.send import send

jobs = ["Amazon", "Walmart", "Target", "Costco", "Home Depot", "Lowe's", "Kroger", "CVS", "Walgreens", "Taco Bell", "McDonald's", "Burger King", "Starbucks", "Subway", "Pizza Hut", "Taco Bell", "McDonald's", "Burger King", "Starbucks", "Subway", "Pizza Hut"]

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Work for money")
    @commands.cooldown(1, 420, commands.BucketType.user)
    async def work_cmd(self, ctx):
        print("Work command called")
        try:
            data = self.db.get_cooldown(ctx.author.id, "last_work")
            if data:
                time_diff = datetime.now().timestamp() - data
                if time_diff < 420:
                    remaining = 420 - time_diff
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    await send(self.bot, ctx, title="Cooldown", content=f"You need to wait {minutes} minutes and {seconds} seconds before working again!", color=0xE74C3C)
                    return

            earned = random.randint(100, 500)
            self.db.add_balance(ctx.author.id, earned)
            self.db.work(ctx.author.id)
            job = random.choice(jobs)
            hours = random.randint(1, 8)
            await send(self.bot, ctx, title="Success", content=f"{ctx.author.mention} has worked at {job} for {hours} hours and earned **${earned}**!", color=0x2ECC71)

        except Exception as e:
            print(f"Error in work command: {e}")
            await send(self.bot, ctx, title="Error", content="An error occurred while processing the work command.", color=0xFF0000)

async def setup(bot):
    work_cog = Work(bot)
    work_cmd = work_cog.work_cmd
    work_cmd.name = "work"
    bot.eco.add_command(work_cmd)
    await bot.add_cog(work_cog)