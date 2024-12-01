import discord
import random
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)
        
    @commands.command(description="Roll dice")
    async def dice_cmd(self, ctx, args):
        try:
            parts = args.split()
            if len(parts) < 2:
                await ctx.send("Usage: >eco dice <bet> <number>\nGuess a number between 2-12")
                return
                
            bet = int(parts[0])
            guess = int(parts[1])
            
            if guess < 2 or guess > 12:
                await ctx.send("Please choose a number between 2 and 12!")
                return
                
            # Roll two dice
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            total = dice1 + dice2
            
            if total == guess:
                winnings = bet * (6 if guess in [2, 12] else 4 if guess in [3, 11] else 2)
                self.db.add_balance(ctx.author.id, winnings)
                await ctx.send(f"🎲 Rolled: {dice1} + {dice2} = {total}\nYou won **${winnings}**!")
            else:
                self.db.remove_balance(ctx.author.id, bet)
                await ctx.send(f"🎲 Rolled: {dice1} + {dice2} = {total}\nYou lost **${bet}**!")
                
        except ValueError:
            await ctx.send("Invalid bet amount! Please use a number.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def setup(bot):
    dice_cog = Dice(bot)
    dice_cmd = dice_cog.dice_cmd
    dice_cmd.name = "dice"
    bot.eco.add_command(dice_cmd)
    await bot.add_cog(dice_cog) 