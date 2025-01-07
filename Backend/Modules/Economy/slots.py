import discord
import random
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore
from Backend.send import send

class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)
        self.symbols = ["🍒", "🍊", "🍋", "🍇", "💎", "7️⃣"]
        self.payouts = {
            "🍒": 2,
            "🍊": 2,
            "🍋": 3,
            "🍇": 4,
            "💎": 5,
            "7️⃣": 10
        }
        
    @commands.command(description="Play slots")
    async def slots_cmd(self, ctx, args):
        try:
            if self.db.get_balance(ctx.author.id) < int(args):
                await send(self.bot, ctx, title="Error", content="You don't have enough money to bet that amount.", color=0xFF0000)
                return

            if not args:
                await send(self.bot, ctx, title="Error", content="Please provide a bet amount.", color=0xFF0000)
                return
            bet = int(args)
            
            results = [random.choice(self.symbols) for _ in range(3)]
            
            if all(x == results[0] for x in results):
                winnings = bet * self.payouts[results[0]]
                self.db.add_balance(ctx.author.id, winnings)
                await send(self.bot, ctx, title="You won!", content=f"🎰 [{' | '.join(results)}]\nJACKPOT! You won **${winnings}**!", color=0x2ECC71)
            else:
                self.db.remove_balance(ctx.author.id, bet)
                await send(self.bot, ctx, title="You lost!", content=f"🎰 [{' | '.join(results)}]\nYou lost **${bet}**!", color=0xE74C3C)
                
        except ValueError:
            await send(self.bot, ctx, title="Error", content="Invalid bet amount! Please use a number.", color=0xFF0000)
        except Exception as e:
            await send(self.bot, ctx, title="Error", content=f"Error: {str(e)}", color=0xFF0000)

async def setup(bot):
    slots_cog = Slots(bot)
    slots_cmd = slots_cog.slots_cmd
    slots_cmd.name = "slots"
    bot.eco.add_command(slots_cmd)
    await bot.add_cog(slots_cog) 