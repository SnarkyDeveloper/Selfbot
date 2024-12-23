from discord.ext import commands
import discord
from main import start_time
import time
from Backend.utils import read_users
users=read_users()['users']
class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Check the bot's uptime", aliases=['uptime', 'stats','info'])
    async def statistics(self, ctx):
        uptime_seconds = time.time() - start_time
        days = int(uptime_seconds // (24 * 3600))  # Calculate days
        hours = int((uptime_seconds % (24 * 3600)) // 3600)  # Calculate hours
        minutes = int((uptime_seconds % 3600) // 60)  # Calculate minutes
        seconds = int(uptime_seconds % 60)  # Calculate seconds
        def uptime(days, hours, minutes, seconds):
            parts = []
            if days:
                parts.append(f"{days} days")
            if hours:
                parts.append(f"{hours} hours")
            if minutes:
                parts.append(f"{minutes} minutes")
            if seconds:
                parts.append(f"{seconds} seconds")
            return ", ".join(parts)
        await ctx.send(f"`Uptime: {uptime(days, hours, minutes, seconds)}`\n`Total Users: {len(users)}`\n`Servers: {len(self.bot.guilds)}`\n`Project: github.com/SnarkyDeveloper/Selfbot (A star is much appreciated ⭐)`")
    @commands.command(description="Pong!")
    async def ping(self, ctx):
        ping = await ctx.send(f"Pong!")
        await ping.edit(content=f"Ping: {round(self.bot.latency*1000)}ms")

async def setup(bot):
    await bot.add_cog(Statistics(bot))