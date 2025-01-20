import discord
import random
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
from Backend.send import send
choices = ["heads", "tails"]

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)
    
    @commands.command(description="Flip a coin", aliases=["cf"])
    async def coinflip_cmd(self, ctx, args):
        try:
            if self.db.get_balance(ctx.author.id) < int(args):
                await send(self.bot, ctx, title="Error", content="You don't have enough money to bet that amount.", color=0xFF0000)
                return

            if not args:
                await send(self.bot, ctx, title="Error", content="Please provide a bet amount.", color=0xFF0000)
                return
            parts = args.split(' ')
            if len(parts) < 1:
                await send(self.bot, ctx, title="Error", content="Please specify a bet amount! Usage: >eco coinflip <amount> [heads/tails]", color=0xFF0000)
                return
                
            bet = int(parts[0])
            choice = parts[1].lower() if len(parts) > 1 else random.choice(choices)
            
            if choice not in choices:
                await send(self.bot, ctx, title="Error", content="Invalid choice! Please use 'heads' or 'tails'", color=0xFF0000)
                return
                
            correct = random.choice(choices)
            if choice == correct:
                self.db.add_balance(ctx.author.id, bet)
                await send(self.bot, ctx, title="You won!", content=f"You won the coinflip! You won **${bet}**", color=0x2ECC71)
            else:
                self.db.remove_balance(ctx.author.id, bet)
                await send(self.bot, ctx, title="You lost!", content=f"You lost **${bet}**! The correct choice was {correct}", color=0xE74C3C)
                
        except ValueError:
            await send(self.bot, ctx, title="Error", content="Invalid bet amount! Please use a number.", color=0xFF0000)
        except Exception as e:
            await send(self.bot, ctx, title="Error", content=f"Error: {str(e)}", color=0xFF0000)

async def setup(bot):
    coinflip_cog = Coinflip(bot)
    coinflip_cmd = coinflip_cog.coinflip_cmd
    coinflip_cmd.name = "coinflip"
    bot.eco.add_command(coinflip_cmd)
    await bot.add_cog(coinflip_cog)