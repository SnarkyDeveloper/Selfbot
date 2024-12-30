import json
from discord.ext import commands
import os
import time
from Backend.send import send
path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

try:
    if not os.path.exists(f'{path}/data/users/afk.json'):
        os.makedirs(f'{path}/data/users', exist_ok=True)
        with open(f'{path}/data/users/afk.json', 'w') as f:
            json.dump({}, f)
except FileNotFoundError:
    os.makedirs(f'{path}/data/users', exist_ok=True)
    with open(f'{path}/data/users/afk.json', 'w') as f:
        json.dump({}, f)

class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='afk', aliases=['brb'])
    async def afk(self, ctx, reason=None):
        reason = reason or "AFK"
        
        with open(f'{path}/data/users/afk.json', 'r') as f:
            afk_data = json.load(f)
        
        if str(ctx.guild.id) not in afk_data:
            afk_data[str(ctx.guild.id)] = {}
        
        afk_data[str(ctx.guild.id)][str(ctx.author.id)] = {
            'reason': reason,
            'timestamp': time.time() * 1000
        }

        with open(f'{path}/data/users/afk.json', 'w') as f:
            json.dump(afk_data, f)
        await send(self.bot, ctx, title='AFK', content=f'{ctx.author.mention} is now AFK: {reason}', color=0x2ECC71)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        with open(f'{path}/data/users/afk.json', 'r') as f:
            afk_data = json.load(f)

        if str(message.author.id) in afk_data.get(str(message.guild.id), {}):
            if not message.content.lower().startswith('>afk') and not message.content.lower().startswith('>brb'):
                afk_time = round((time.time() * 1000 - afk_data[str(message.guild.id)][str(message.author.id)]['timestamp']) / 1000)
                del afk_data[str(message.guild.id)][str(message.author.id)]

                with open(f'{path}/data/users/afk.json', 'w') as f:
                    json.dump(afk_data, f)

                minutes, seconds = divmod(afk_time, 60)
                hours, minutes = divmod(minutes, 60)

                deletable = await send(self.bot, message, title='AFK', content=f"Welcome back {message.author.mention}! You were AFK for {hours} hours, {minutes} minutes, and {seconds} seconds.")
                await deletable.delete(delay=15)
        if message.mentions:
            for user in message.mentions:
                if str(user.id) in afk_data.get(str(message.guild.id), {}):
                    reason = afk_data[str(message.guild.id)][str(user.id)]['reason']
                    await send(self.bot, message, title='AFK', content=f"{user.name} is AFK with reason: {reason}")

async def setup(bot):
    await bot.add_cog(Afk(bot))
