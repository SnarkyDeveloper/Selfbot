import re
from discord.ext import commands
from PyMultiDictionary import MultiDictionary
dictionary = MultiDictionary()
from Backend.send import send
class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Define a word', aliases=['def'])
    async def define(self, ctx, id=None):
        if ctx.message.startswith(">def "):
            ctx2 = ctx.message.content.replace(">def ", "", 1).strip()
        else:
            ctx2 = ctx.message.content.replace(">define ", "", 1).strip()
        if ctx.message.reference:
            id = ctx.message.reference.message_id
        elif id is None and not ctx2:
            await send(self.bot, ctx, title='Error', content="Please provide a message ID or reply to a message", color=0xFF0000)
            return
        elif ctx2: 
            message = ctx2
        else:
            id = ctx.message.id
        
        if id and isinstance(id, int):
            message = (await ctx.fetch_message(id)).content if await ctx.fetch_message(id) else None
        
        if message:
            definition = dictionary.meaning('en', message)
            if not definition[1]:
                await send(self.bot, ctx, title='Error', content="Definition not found", color=0xFF0000)
            else:
                result = ''.join(c for c in definition[0] if c.isalpha() or c.isspace())
                await send(self.bot, ctx, title=message.title(), content=f'**Type:** {result} \n\n**Definition:** {definition[1]}', color=0x2ECC71)
        else:
            await send(self.bot, ctx, title='Error', content="Message not found", color=0xFF0000)

async def setup(bot):
    await bot.add_cog(Define(bot))