import discord
from discord.ext import commands
from Backend.send import send
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', description="Shows this message")
    async def help_command(self, ctx, page: int = 1):
        try:
            commands_list = [f"`{command.name}`: {command.description}" for command in self.bot.commands]
            end = page * 10
            start = end - 10
            page_commands = commands_list[start:end]
            response = "Available commands:\n" + "\n".join(page_commands)
            await send(self.bot, ctx, title=f'Help Page {page}', content=response)
        except Exception as e:
            print(f"Error in help command: {e}")
            
async def setup(bot):
    await bot.add_cog(Help(bot))

