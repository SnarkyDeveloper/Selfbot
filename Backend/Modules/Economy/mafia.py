import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
import random
from datetime import datetime

mafia_phrases = ["has helped with a drug deal", "has helped with a robbery", "has helped with a kidnapping", "has helped with a hit", "has helped with a murder", "has helped with a extortion", "has helped with a blackmail", "has helped with a prostitution ring", "has helped with a human trafficking ring", "has helped with a arms dealing", "has helped with a arms smuggling", "has helped with a arms trafficking", "has helped with a arms manufacturing", "has helped with a arms dealing", "has helped with a arms smuggling", "has helped with a arms trafficking", "has helped with a arms manufacturing"]

class Mafia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Work with the mafia")
    @commands.cooldown(1, 300, commands.BucketType.user)  # 5 minutes
    async def mafia_cmd(self, ctx): 
        try:
            data = self.db.get_cooldown(ctx.author.id, "last_mafia")
            if data:
                time_diff = datetime.now().timestamp() - data
                if time_diff < 300:  # 5 minutes in seconds
                    remaining = 300 - time_diff
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    await ctx.send(f"You need to wait {minutes} minutes and {seconds} seconds before doing another mafia job!")
                    return

            caught = random.randint(1, 100)
            if caught <= 10:
                self.db.remove_balance(ctx.author.id, 1000)
                await ctx.send(f"{ctx.author.mention} was caught by the police and was fined $1000!")
            else:
                money = random.randint(1000, 5000)
                self.db.add_balance(ctx.author.id, money)
                await ctx.send(f"{ctx.author.mention} {random.choice(mafia_phrases)} and earned **${money}**!")

            # Update mafia cooldown
            data = self.db.read_eco()
            for entry in data["users"]:
                if entry["user"] == str(ctx.author.id):
                    entry["last_mafia"] = datetime.now().timestamp()
                    self.db.write_eco(data)
                    return

        except Exception as e:
            print(f"Error in mafia command: {e}")
            await ctx.send("An error occurred while processing the mafia command.")

async def setup(bot):
    mafia_cog = Mafia(bot)
    mafia_cmd = mafia_cog.mafia_cmd
    mafia_cmd.name = "mafia"
    bot.eco.add_command(mafia_cmd)
    await bot.add_cog(mafia_cog)
