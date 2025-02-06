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

    @commands.command(name='afk', aliases=['brb'], description='Go AFK')
    async def afk(self, ctx, reason=None):
        reason = reason or "AFK"
        
        with open(f'{path}/data/users/afk.json', 'r') as f:
            afk_data = json.load(f)
        
        guild = str(ctx.guild.id if ctx.guild else 'DM')
        if guild not in afk_data:
            afk_data[guild] = {}
        afk_data[guild][str(ctx.author.id)] = {
            'reason': reason,
            'timestamp': int(time.time())
        }

        with open(f'{path}/data/users/afk.json', 'w') as f:
            json.dump(afk_data, f)
        await send(self.bot, ctx, title=f'{ctx.author.display_name} now AFK: {reason}', color=0x2ECC71)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.bot.get_context(message)

        with open(f'{path}/data/users/afk.json', 'r') as f:
            afk_data = json.load(f)

        guild = str(message.guild.id if message.guild else 'DM')
        if str(message.author.id) in afk_data.get(guild, {}):
            if not message.content.lower().startswith('>afk') and not message.content.lower().startswith('>brb'):
                afk_time = afk_data[guild][str(message.author.id)]['timestamp']
                del afk_data[guild][str(message.author.id)]
                try:
                    deletable = await send(self.bot, ctx, title=f'Welcome Back {message.author.display_name}, you were AFK since <t:{afk_time}:R>', color=0xFEE75C)
                except Exception as e:
                    print(f"Error: {e}")
                with open(f'{path}/data/users/afk.json', 'w') as f:
                    json.dump(afk_data, f)

                await deletable.delete(delay=15)
        if message.mentions:
            for user in message.mentions:
                if str(user.id) in afk_data.get(guild, {}):
                    reason = afk_data[guild][str(user.id)]['reason']
                    afk_time = afk_data[guild][str(user.id)]['timestamp']

                    await send(self.bot, ctx, title=f"{user.display_name} is AFK with reason: {reason} since <t:{afk_time}:R>", color=0xFEE75C)

async def setup(bot):
    await bot.add_cog(Afk(bot))
