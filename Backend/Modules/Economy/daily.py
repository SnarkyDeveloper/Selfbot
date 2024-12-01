import discord
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
from datetime import datetime, timedelta

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Claim your daily reward")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily_cmd(self, ctx):
        try:
            data = self.db.get_cooldown(ctx.author.id, "last_daily")
            if data:
                time_diff = datetime.now().timestamp() - data
                if time_diff < 86400:  # 24 hours in seconds
                    remaining = 86400 - time_diff
                    hours = int(remaining // 3600)
                    minutes = int((remaining % 3600) // 60)
                    await ctx.send(f"You can claim your daily reward again in {hours} hours and {minutes} minutes!")
                    return

            # If cooldown passed or no previous daily claim
            self.db.add_balance(ctx.author.id, 100)  # Add 100 to balance
            await self.db.daily(ctx.author.id)  # Update last_daily timestamp
            await ctx.send(f"{ctx.author.mention}, you have claimed your daily reward of $100! Come back in 24 hours to claim another one!")

        except commands.CommandOnCooldown as e:
            hours = int(e.retry_after // 3600)
            minutes = int((e.retry_after % 3600) // 60)
            await ctx.send(f"You can claim your daily reward again in {hours} hours and {minutes} minutes!")
        except Exception as e:
            print(f"Error in daily command: {e}")
            await ctx.send("An error occurred while processing the daily command.")

async def setup(bot):
    daily_cog = Daily(bot)
    daily_cmd = daily_cog.daily_cmd
    daily_cmd.name = "daily"  # Set the command name
    bot.eco.add_command(daily_cmd)  # Add it to the eco group
    await bot.add_cog(daily_cog)