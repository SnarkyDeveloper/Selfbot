import discord
import random
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
from Backend.send import send
class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)
        
    @commands.command(description="Roll dice")
    async def dice_cmd(self, ctx, args):
        try:
            if self.db.get_balance(ctx.author.id) < int(args):
                await send(self.bot, ctx, title="Error", content="You don't have enough money to bet that amount.", color=0xFF0000)
                return

            if not args:
                await send(self.bot, ctx, title="Error", content= "Please provide a bet amount.", color=0xFF0000)
                return
            parts = args.split()
            if len(parts) < 2:
                await send(self.bot, ctx, title="Error", content="Usage: >eco dice <bet> <number>\nGuess a number between 2-12", color=0xFF0000)
                return
                
            bet = int(parts[0])
            guess = int(parts[1])
            
            if guess < 2 or guess > 12:
                await send(self.bot, ctx, title="Error", content="Please choose a number between 2 and 12!", color=0xFF0000)
                return
                
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            total = dice1 + dice2
            
            if total == guess:
                winnings = bet * (6 if guess in [2, 12] else 4 if guess in [3, 11] else 2)
                self.db.add_balance(ctx.author.id, winnings)
                await send(self.bot, ctx, title="You won!", content=f"🎲 Rolled: {dice1} + {dice2} = {total}\nYou won **${winnings}**!", color=0x2ECC71)
            else:
                self.db.remove_balance(ctx.author.id, bet)
                await send(self.bot, ctx, title="You lost!", content=f"🎲 Rolled: {dice1} + {dice2} = {total}\nYou lost **${bet}**!", color=0xE74C3C)
                
        except ValueError:
            await send(self.bot, ctx, title="Error", content="Invalid bet amount! Please use a number.", color=0xFF0000)
        except Exception as e:
            await send(self.bot, ctx, title="Error", content=f"Error: {str(e)}", color=0xFF0000)

async def setup(bot):
    dice_cog = Dice(bot)
    dice_cmd = dice_cog.dice_cmd
    dice_cmd.name = "dice"
    bot.eco.add_command(dice_cmd)
    await bot.add_cog(dice_cog) 