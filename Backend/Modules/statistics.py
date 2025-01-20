from discord.ext import commands
import discord
from main import start_time
import time
from Backend.utils import read_users
from Backend.send import send
class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Check the bot's uptime", aliases=['uptime', 'stats','info'])
    async def statistics(self, ctx):
        commands = len(self.bot.commands)
        users=read_users()['users']
        servers = read_users()['guilds']
        uptime_seconds = time.time() - start_time
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
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
        await send(self.bot, ctx, title="Statistics", content=f"Uptime: {uptime(days, hours, minutes, seconds)}\nTotal Users: {len(users)}\nServers: {len(servers)}\nTotal Commands: {commands}\nProject: github.com/SnarkyDeveloper/Selfbot (Please star ⭐)")
    @commands.command(description="Pong!")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000, 2)
        if latency < 150:
            await send(self.bot, ctx, title='Pong!', content=f'Latency: {latency} ms', color=0x2ECC71)
        elif latency < 500:
            await send(self.bot, ctx, title='Pong!', content=f'Latency: {latency} ms', color=0xFEE75C)
        else:
            await send(self.bot, ctx, title='Pong!', content=f'Latency: {latency} ms', color=0xE74C3C)

async def setup(bot):
    await bot.add_cog(Statistics(bot))