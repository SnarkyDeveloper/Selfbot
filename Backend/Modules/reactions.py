import discord
import httpx
from discord.ext import commands
import random
import json
from Backend.send import send
class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sources = ['https://nekos.life/api/v2/img', 'https://api.waifu.pics/sfw', 'https://purrbot.site/api/img/sfw']

    async def get_reaction(self, reaction, source=None):
        try:
            if source:
                url = source
            else:
                url = random.choice(self.sources)
            if url != 'https://purrbot.site/api/img/sfw':
                response = json.loads(httpx.get(f'{url}/{reaction}').text)
                return response['url']
            else:
                response = json.loads(httpx.get(f'{url}/{reaction}/gif').text)
                return response['link']
        except:
            reaction =  await self.get_reaction(reaction)
            return reaction 

    @commands.command(description='Kiss a user!')
    async def kiss(self, ctx, user: discord.Member = None):
        reaction = await self.get_reaction('kiss')
        if not user:
            await send(self.bot, ctx, title=f'{ctx.author.global_name} kisses... themselves?',color=0xFEE75C, content=f'{ctx.author.mention} kisses themselves! How strange!', image=reaction)
        else:
            await send(self.bot, ctx, color=0xFEE75C, title=f'{ctx.author.global_name} kisses {user.mention}!', content=f'{ctx.author.mention} kisses {user.mention}, How cute!', image=reaction)

    @commands.command(description='Hug a user!')
    async def hug(self, ctx, user: discord.Member = None):
        reaction = await self.get_reaction('hug')
        if not user:
            await send(self.bot, ctx, title=f'{ctx.author.global_name} hugs... themselves?', color=0xFEE75C, content=f'{ctx.author.mention} hugs themselves! How strange!', image=reaction)
        else:
            await send(self.bot, ctx, color=0xFEE75C, title=f'{ctx.author.global_name} hugs {user.mention}!',content=f'{ctx.author.mention} hugs {user}, How cute!', image=reaction)

    @commands.command(description='Tickle a user!')
    async def tickle(self, ctx, user: discord.Member = None):
        if not user:
            await send(self.bot, ctx, color=0xFF0000, title=f'Error', content=f'{ctx.author.mention} You can\'t tickle yourself!')
        else:
            reaction = await self.get_reaction('tickle')
            await send(self.bot, ctx, color=0xFEE75C, title=f'Tickles',content=f'{ctx.author.mention} tickles {user}!', image=reaction)

    @commands.command(description='Bite a user!')
    async def bite(self, ctx, user: discord.Member = None):
        if not user:
            await send(self.bot, ctx, color=0xFF0000, title='Error', content=f'{ctx.author.mention} You can\'t bite yourself!')
        else:
            reaction = await self.get_reaction('bite')
            await send(self.bot, ctx, color=0xFEE75C, title=f'Someone is feeling feisty',content=f'{ctx.author.mention} bit {user}!', image=reaction)

    @commands.command(description='Slap a user!')
    async def slap(self, ctx, user: discord.Member = None):
        if not user:
            await send(self.bot, ctx, color=0xFF0000, title='Error', content=f'{ctx.author.mention} You can\'t slap yourself!')
        else:
            reaction = await self.get_reaction('slap')
            await send(self.bot, ctx, color=0xFEE75C, title=f'Someone is angry', content=f'{ctx.author.mention} slapped {user}!', image=reaction)

    @commands.command(description='Blush!')
    async def blush(self, ctx, user: discord.Member = None):
        reaction = await self.get_reaction('blush', source='https://purrbot.site/api/img/sfw')
        if user:
            await send(self.bot, ctx, color=0xFEE75C, title=f'Someone\'s blushing!', content=f'{ctx.author.mention} has a crush on {user} (probably) :3', image=reaction)
        else:
            await send(self.bot, ctx, color=0xFEE75C, title='Someone\'s blushing!', content=f'{ctx.author.mention} is blushing!', image=reaction)

async def setup(bot):
    await bot.add_cog(Reactions(bot))


