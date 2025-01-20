import discord
from discord.ext import commands
import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import x, y, z
from Backend.send import send
class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='calc', description='Calculate mathematical expressions')
    async def calculate(self, ctx, expression):
        try:
            expression = expression.replace('^', '**')
            
            result = parse_expr(expression)
            
            simplified = sympy.simplify(result)
            
            try:
                numeric_result = float(simplified.evalf())
                if numeric_result.is_integer():
                    await send(self.bot, ctx, title="Result", content=f"{int(numeric_result)}", color=0x2ECC71)
                else:
                    await send(self.bot, ctx, title="Result", content=f"{numeric_result}", color=0x2ECC71)
            except:
                await send(self.bot, ctx, title="Result", content=f"{simplified}", color=0x2ECC71)
                
        except Exception as e:
            await send(self.bot, ctx, title="Calculator Error", content=f"Error: Could not evaluate expression. Make sure it's properly formatted.", color=0xff0000)


async def setup(bot):
    await bot.add_cog(Calculator(bot))