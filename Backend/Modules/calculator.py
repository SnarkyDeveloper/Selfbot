import discord
from discord.ext import commands
import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import x, y, z

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
                    await ctx.send(f"Result: {int(numeric_result)}")
                else:
                    await ctx.send(f"Result: {numeric_result}")
            except:
                await ctx.send(f"Result: {simplified}")
                
        except Exception as e:
            await ctx.send(f"Error: Could not evaluate expression. Make sure it's properly formatted.")
            print(f"Calculator error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Calculator(bot))