import discord
from discord.ext import commands

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = [u"1️⃣", u"2️⃣", u"3️⃣", u"4️⃣", u"5️⃣", u"6️⃣", u"7️⃣", u"8️⃣", u"9️⃣", u"🔟"]

    @commands.command()
    async def poll(self, ctx, content: str):
        if ':' not in content:
            await ctx.send("Please provide a question followed by options, separated by a colon.")
            return
        
        question, options_str = content.split(":", 1)
        question = question.strip() and question.capitalize()
        options = [opt.strip() for opt in options_str.split(",")]

        if len(options) < 2:
            await ctx.send("Please provide at least two options.")
            return
        if len(options) > 10:
            await ctx.send("You can only have up to 10 options.")
            return
        
        options_str = "\n".join([f"{i}. `{options[i]}`" for i in range(len(options))])

        poll = await ctx.send(f"# {question}\n{options_str}")
        
        for i in range(len(options)):
            await poll.add_reaction(self.reactions[i])

async def setup(bot):
    await bot.add_cog(Polls(bot))
