import re
from discord.ext import commands
from PyMultiDictionary import MultiDictionary
dictionary = MultiDictionary()
from Backend.send import send
class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Define a word', aliases=['def'])
    async def define(self, ctx, word=None):
        if ctx.message.reference:
            ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            word = word or ref_message.content.strip()
        elif word is None:
            await send(self.bot, ctx, title='Error', content="Please reply to a message or provide a word.", color=0xFF0000)
            return

        try:
            definition = dictionary.meaning('en', word)
        except Exception as e:
            await send(self.bot, ctx, title='Error', content=f"An error occurred while fetching the definition: {e}", color=0xFF0000)
            return

        if not definition or not definition[1]:
            await send(self.bot, ctx, title='Error', content="Definition not found.", color=0xFF0000)
        else:
            word_type = ''.join(c for c in definition[0] if c.isalpha() or c.isspace())
            await send(self.bot, ctx, title=word.title(), content=f'**Type:** {word_type}\n\n**Definition:** {definition[1]}', color=0x2ECC71)

async def setup(bot):
    await bot.add_cog(Define(bot))