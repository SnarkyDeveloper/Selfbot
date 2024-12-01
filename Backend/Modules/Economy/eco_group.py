from discord.ext import commands

def create_eco_group(bot):
    eco_group = commands.Group(name='eco', invoke_without_command=True)
    
    @eco_group.command()
    async def help(ctx):
        """Economy commands"""
        await ctx.send("Available commands: work, daily, balance, steal, shop")
    
    bot.add_command(eco_group)
    return eco_group 