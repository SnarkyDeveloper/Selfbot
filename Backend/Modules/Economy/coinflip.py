import discord
import random
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
choices = ["heads", "tails"]

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)
    
    @commands.command(description="Flip a coin", aliases=["cf"])
    async def coinflip_cmd(self, ctx, args):
        try:
            # Split the args into bet and choice
            parts = args.split()
            if len(parts) < 1:
                await ctx.send("Please specify a bet amount! Usage: >eco coinflip <amount> [heads/tails]")
                return
                
            bet = int(parts[0])
            choice = parts[1].lower() if len(parts) > 1 else random.choice(choices)
            
            if choice not in choices:
                await ctx.send("Invalid choice! Please use 'heads' or 'tails'")
                return
                
            correct = random.choice(choices)
            if choice == correct:
                self.db.add_balance(ctx.author.id, bet)
                await ctx.send(f"You won the coinflip! You won **${bet}**")
            else:
                self.db.remove_balance(ctx.author.id, bet)
                await ctx.send(f"You lost **${bet}**! The correct choice was {correct}")
                
        except ValueError:
            await ctx.send("Invalid bet amount! Please use a number.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def setup(bot):
    coinflip_cog = Coinflip(bot)
    coinflip_cmd = coinflip_cog.coinflip_cmd
    coinflip_cmd.name = "coinflip"
    bot.eco.add_command(coinflip_cmd)
    await bot.add_cog(coinflip_cog)