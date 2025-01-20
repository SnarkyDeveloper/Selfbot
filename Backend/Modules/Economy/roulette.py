import discord
import random
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
from Backend.send import send

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)
        
    @commands.command(description="Play roulette", aliases=["rl"])
    async def roulette_cmd(self, ctx, args):
        try:
            if self.db.get_balance(ctx.author.id) < int(args):
                await send(self.bot, ctx, title="Error", content="You don't have enough money to bet that amount.", color=0xFF0000)
                return

            if not args:
                await send(self.bot, ctx, title="Error", content="Please provide a bet amount.", color=0xFF0000)
                return
            parts = args.split()
            if len(parts) < 2:
                await send(self.bot, ctx, title="Error", content="Usage: >eco roulette <bet> <choice>\nChoices: red/black/green or number (0-36)", color=0xFF0000)
                return
            
            bet = int(parts[0])
            choice = parts[1].lower()
            
            result = random.randint(0, 36)
            
            red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
            black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
            
            if choice.isdigit():
                if int(choice) == result:
                    winnings = bet * 35
                    self.db.add_balance(ctx.author.id, winnings)
                    await send(self.bot, ctx, title="You won!", content=f"🎲 The ball landed on {result}! You won **${winnings}**!", color=0x2ECC71)
                    return
            elif choice == "red" and result in red:
                self.db.add_balance(ctx.author.id, bet)
                await send(self.bot, ctx, title="You Won!", content=f"🎲 The ball landed on {result} (red)! You won **${bet}**!", color=0x2ECC71)
                return
            elif choice == "black" and result in black:
                self.db.add_balance(ctx.author.id, bet)
                await send(self.bot, ctx, title="You Won!", content=f"🎲 The ball landed on {result} (black)! You won **${bet}**!", color=0x2ECC71)
                return
            elif choice == "green" and result == 0:
                winnings = bet * 35
                self.db.add_balance(ctx.author.id, winnings)
                await send(self.bot, ctx, title="You Won!", content=f"🎲 The ball landed on 0 (green)! You won **${winnings}**!", color=0x2ECC71)
                return
                
            self.db.remove_balance(ctx.author.id, bet)
            color = "red" if result in red else "black" if result in black else "green"
            await send(self.bot, ctx, title="You lost!", content=f"🎲 The ball landed on {result} ({color})! You lost **${bet}**!", color=0xE74C3C)
            
        except ValueError:
            await send(self.bot, ctx, title="Error", content="Invalid bet amount! Please use a number.", color=0xFF0000)
        except Exception as e:
            await send(self.bot, ctx, title="Error", content=f"Error: {str(e)}", color=0xFF0000)

async def setup(bot):
    roulette_cog = Roulette(bot)
    roulette_cmd = roulette_cog.roulette_cmd
    roulette_cmd.name = "roulette"
    bot.eco.add_command(roulette_cmd)
    await bot.add_cog(roulette_cog)
