from Backend.Modules.ecoCore import Economy as EcoCore
from discord.ext import commands
import discord
from Backend.send import send
class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Check your balance", aliases=["bal"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance_cmd(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        else:
            user = await commands.UserConverter().convert(ctx, user)
        try:
            self.db.user_exists(user.id)
            balance = self.db.get_balance(user.id)
            print(f"Retrieved balance for {user} (ID: {user.id}): ${balance}")
            await send(self.bot, ctx, title=f"{user.display_name}'s Balance", content=f"{user.mention}'s balance is **${balance:,}**", color=0x2ECC71)
        except Exception as e:
            print(f"Error in balance command: {e}")
            await send(self.bot, ctx, title="Error", content="An error occurred while checking the balance.", color=0xFF0000)

async def setup(bot):
    balance_cog = Balance(bot)
    balance_cmd = balance_cog.balance_cmd
    balance_cmd.name = "balance"
    bot.eco.add_command(balance_cmd)
    await bot.add_cog(balance_cog)