import re
from discord.ext import commands
from Backend.utils import check_permissions
from PyMultiDictionary import MultiDictionary
dictionary = MultiDictionary()
class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Define a word', aliases=['def'])
    async def define(self, ctx, id=None):
        ctx2 = ctx.message.content.replace(">def ", "", 1).strip()
        if check_permissions(ctx.author):
            if ctx.message.reference:
                id = ctx.message.reference.message_id
            elif id is None and not ctx2:
                await ctx.send("Please provide a message ID or reply to a message")
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
                    await ctx.send("Definition not found")
                else:
                    result = ''.join(c for c in definition[0] if c.isalpha() or c.isspace())
                    await ctx.send(f'# {message.title()}: \n**Type:** {result} \n**Definition:** {definition[1]}')
            else:
                await ctx.send("Message not found")

async def setup(bot):
    await bot.add_cog(Define(bot))