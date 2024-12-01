from Backend.Modules.ecoCore import Economy as EcoCore
from discord.ext import commands
import discord

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)

    @commands.command(description="Check your balance", aliases=["bal"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance_cmd(self, ctx, user: discord.Member = None):
        print(f"Balance command called with user: {user}")
        if user is None:
            user = ctx.author
        try:
            # Ensure user exists in database
            self.db.user_exists(user.id)
            balance = self.db.get_balance(user.id)
            print(f"Retrieved balance for {user} (ID: {user.id}): ${balance}")
            await ctx.send(f"{user.mention}'s balance is **${balance:,}**")
        except Exception as e:
            print(f"Error in balance command: {e}")
            await ctx.send("An error occurred while checking the balance.")

async def setup(bot):
    balance_cog = Balance(bot)
    balance_cmd = balance_cog.balance_cmd
    balance_cmd.name = "balance"
    bot.eco.add_command(balance_cmd)
    await bot.add_cog(balance_cog)