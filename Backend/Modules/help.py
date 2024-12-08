import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', description="Shows this message")
    async def help_command(self, ctx):
        print("Help command invoked")
        try:
            commands_list = [f"`{command.name}`: {command.description}" for command in self.bot.commands]
            response = "Available commands:\n" + "\n".join(commands_list)
            await ctx.send(response)
        except Exception as e:
            print(f"Error in help command: {e}")
            
async def setup(bot):
    await bot.add_cog(Help(bot))
