import json
from discord.ext import commands
import os
import time
path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
try:
    if os.path.exists(f'{path}/data/users/afk.json'):
        pass
except FileNotFoundError:
    os.makedirs(f'{path}/data/users', exist_ok=True)
    with open(f'{path}/data/users/afk.json', 'w') as f:
        json.dump({}, f)
class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='afk', aliases=['brb'])
    async def afk(self, ctx, reason=None):
        if reason is None:
            reason = "AFK"
        with open(f'{path}/data/users/afk.json', 'r') as f:
            afk_data = json.load(f)
        afk_data[str(ctx.author.id)] = {
            'reason': reason,
            'timestamp': time.time()*1000
        }

        with open(f'{path}/data/users/afk.json', 'w') as f:
            json.dump(afk_data, f)

        await ctx.send(f'{ctx.author.display_name} is now AFK: {reason}')
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        with open(f'{path}/data/users/afk.json', 'r') as f:
            afk_data = json.load(f)
        if str(message.author.id) in afk_data:
            if not message.content.startswith('>afk'):
                afk_time = round((time.time()*1000 - afk_data[str(message.author.id)]['timestamp'])/1000)
                del afk_data[str(message.author.id)]
                with open(f'{path}/data/users/afk.json', 'w') as f:
                    json.dump(afk_data, f)
                minutes, seconds = divmod(afk_time, 60)
                hours, minutes = divmod(minutes, 60)
                await message.channel.send(f"Welcome back {message.author.mention}! You were AFK for {hours} hours, {minutes} minutes and {seconds} seconds.")

        if message.mentions:
            for user in message.mentions:
                if str(user.id) in afk_data:
                    reason = afk_data[str(user.id)]['reason']
                    await message.channel.send(f"{user.name} is AFK with reason: {reason}")
async def setup(bot):
    await bot.add_cog(Afk(bot))