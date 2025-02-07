import discord
import httpx
from discord.ext import commands
import random
import json
from Backend.send import send
class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sources = ['https://nekos.life/api/v2/img', 'https://api.waifu.pics/sfw', 'https://purrbot.site/api/img/sfw', 'https://api.otakugifs.xyz/gif']

    async def get_reaction(self, reaction, source=None):
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                url = source if source else random.choice(self.sources)
            
                if url == 'https://purrbot.site/api/img/sfw':
                    response = await client.get(f'{url}/{reaction}/gif')
                    data = response.json()
                    return data['link']
                elif url == 'https://api.otakugifs.xyz/gif':
                    response = await client.get(f'{url}/?reaction={reaction}')
                    data = response.json()
                    return data['url']
                response = await client.get(f'{url}/{reaction}')
                data = response.json()
                return data['url']
            
            except (httpx.RequestError, json.JSONDecodeError, KeyError):
                if source:
                    return await self.get_reaction(reaction, None)
                remaining_sources = [s for s in self.sources if s != url]
                if remaining_sources:
                    return await self.get_reaction(reaction, random.choice(remaining_sources))
                raise Exception("All reaction sources failed")

    @commands.command(description='Kiss a user!')
    async def kiss(self, ctx, user: discord.Member = None):
        reaction = await self.get_reaction('kiss')
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        if not user or user == ctx.author:
            await send(self.bot, ctx, title=f'{ctx.author.display_name} kisses... themselves?',color=0xFEE75C, content=f'{ctx.author.mention} kisses themselves! How strange!', image=reaction)
        else:
            await send(self.bot, ctx, color=0xFEE75C, title=f'{ctx.author.display_name} kisses {user.display_name}!', content=f'{ctx.author.mention} kisses {user.mention}, How cute!', image=reaction)

    @commands.command(description='Hug a user!')
    async def hug(self, ctx, user: discord.Member = None):
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        reaction = await self.get_reaction('hug')
        if not user or user == ctx.author:
            await send(self.bot, ctx, title=f'{ctx.author.display_name} hugs... themselves?', color=0xFEE75C, content=f'{ctx.author.mention} hugs themselves! How strange!', image=reaction)
        else:
            await send(self.bot, ctx, color=0xFEE75C, title=f'{ctx.author.display_name} hugs {user.display_name}!',content=f'{ctx.author.mention} hugs {user.mention}, How cute!', image=reaction)

    @commands.command(description='Tickle a user!')
    async def tickle(self, ctx, user: discord.Member = None):
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        if not user or user == ctx.author:
            await send(self.bot, ctx, color=0xFF0000, title=f'Error', content=f'{ctx.author.mention} You can\'t tickle yourself!')
        else:
            reaction = await self.get_reaction('tickle')
            await send(self.bot, ctx, color=0xFEE75C, title=f'Hehe that tickles',content=f'{ctx.author.mention} tickles {user.mention}!', image=reaction)

    @commands.command(description='Bite a user!')
    async def bite(self, ctx, user: discord.Member = None):
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        if not user or user == ctx.author:
            await send(self.bot, ctx, color=0xFF0000, title='Error', content=f'{ctx.author.mention} You can\'t bite yourself!')
        else:
            reaction = await self.get_reaction('bite')
            await send(self.bot, ctx, color=0xFEE75C, title=f'Someone is feeling feisty',content=f'{ctx.author.mention} bit {user.mention}!', image=reaction)

    @commands.command(description='Slap a user!')
    async def slap(self, ctx, user: discord.Member = None):
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        if not user or user == ctx.author:
            await send(self.bot, ctx, color=0xFF0000, title='Error', content=f'{ctx.author.mention} You can\'t slap yourself!')
        else:
            reaction = await self.get_reaction('slap')
            await send(self.bot, ctx, color=0xFEE75C, title=f'Someone\'s angry', content=f'{ctx.author.mention} slapped {user.mention}!', image=reaction)

    @commands.command(description='Blush!')
    async def blush(self, ctx, user: discord.Member = None):
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        reaction = await self.get_reaction('blush', source='https://purrbot.site/api/img/sfw')
        if user:
            await send(self.bot, ctx, color=0xFEE75C, title=f'Someone\'s blushing!', content=f'{ctx.author.mention} has a crush on {user.mention} (probably) :3', image=reaction)
        else:
            await send(self.bot, ctx, color=0xFEE75C, title='Someone\'s blushing!', content=f'{ctx.author.mention} is blushing!', image=reaction)
    @commands.command(description='Poke!')
    async def poke(self, ctx, user: discord.Member = None):
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        reaction = await self.get_reaction('poke')
        if not user or user == ctx.author:
            await send(self.bot, ctx, color=0xFF0000, title='Error', content=f'{ctx.author.mention} You can\'t poke yourself!')
        else:
            await send(self.bot, ctx, color=0xFEE75C, title=f'ouchie :c', content=f'{ctx.author.mention} poked {user.mention}', image=reaction)
    @commands.command(description='Cuddle someone!')
    async def cuddle(self, ctx, user: discord.Member = None):
        if user:
            user = await commands.UserConverter().convert(ctx, user)
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            user = ref_message.author
        reaction = await self.get_reaction('cuddle')
        if not user or user == ctx.author:
            await send(self.bot, ctx, color=0xFF0000, title='Error', content=f'{ctx.author.mention} You can\'t cuddle yourself! Sorry single folk')
        else:
            await send(self.bot, ctx, color=0xFEE75C, title=f'mmm that\'s warm', content=f'{ctx.author.mention} is cuddling {user.mention}', image=reaction)
async def setup(bot):
    await bot.add_cog(Reactions(bot))